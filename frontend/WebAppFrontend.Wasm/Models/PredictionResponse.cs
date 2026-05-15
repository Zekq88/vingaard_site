using System.Text.Json.Serialization;

namespace WebAppFrontend.Wasm.Models;

public class PredictionResponse
{
    [JsonPropertyName("filename")]
    public string Filename {get; set;} = "";

    [JsonPropertyName("label")]
    public string Label {get; set;} = ""; 

    [JsonPropertyName("confidence")]
    public double Confidence {get; set;}


    [JsonPropertyName("all_probs")]    
    public Dictionary<string, float> AllProbs {get; set;} = new();
}