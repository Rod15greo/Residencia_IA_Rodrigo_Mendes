using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine.Networking;

public class VoiceRecorder : MonoBehaviour
{
    public Button startButton;
    public Button stopButton;
    public TextMeshProUGUI transcriptText;

    private AudioSource audioSource;
    private string microphoneName;
    private AudioClip recordedClip;

    void Start()
    {
        startButton.onClick.AddListener(StartRecording);
        stopButton.onClick.AddListener(StopRecording);
        audioSource = gameObject.AddComponent<AudioSource>();
        microphoneName = Microphone.devices[0];
    }

    void StartRecording()
    {
        recordedClip = Microphone.Start(microphoneName, false, 10, 44100);
        audioSource.clip = recordedClip;
    }

    void StopRecording()
    {
        Microphone.End(microphoneName);
        StartCoroutine(ProcessAudio());
    }

    IEnumerator ProcessAudio()
    {
        string filePath = Path.Combine(Application.persistentDataPath, "recordedAudio.wav");

        // Save the recorded audio to a file
        SaveWavFile(filePath, recordedClip);

        // Send the audio file to Google Speech-to-Text API
        string transcription = yield return StartCoroutine(SendAudioToGoogle(filePath));
        transcriptText.text = transcription;
    }

    void SaveWavFile(string filePath, AudioClip clip)
    {
        var samples = new float[clip.samples];
        clip.GetData(samples, 0);
        byte[] wavFile = WavUtility.FromAudioClip(clip, filePath, false);
        File.WriteAllBytes(filePath, wavFile);
    }

    IEnumerator SendAudioToGoogle(string filePath)
    {
        byte[] audioData = File.ReadAllBytes(filePath);
        string base64Audio = System.Convert.ToBase64String(audioData);

        var request = new UnityWebRequest("https://speech.googleapis.com/v1/speech:recognize?key=YOUR_API_KEY", "POST");
        request.uploadHandler = new UploadHandlerRaw(System.Text.Encoding.UTF8.GetBytes("{\"config\":{\"encoding\":\"LINEAR16\",\"sampleRateHertz\":44100,\"languageCode\":\"en-US\"},\"audio\":{\"content\":\"" + base64Audio + "\"}}"));
        request.downloadHandler = new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");

        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.Success)
        {
            string jsonResponse = request.downloadHandler.text;
            var json = SimpleJSON.JSON.Parse(jsonResponse);
            string transcription = json["results"][0]["alternatives"][0]["transcript"];
            yield return transcription;
        }
        else
        {
            Debug.LogError("Error in speech recognition: " + request.error);
            yield return null;
        }
    }
}
