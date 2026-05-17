using System.Net.Http.Headers;
using System.Net.Http.Json;
using WebAppFrontend.Wasm.Models;

namespace WebAppFrontend.Wasm.Services;

public class PredictionClient
{
    private readonly HttpClient _http;
    private const string ApiUrl = "/api/predict/";

    public PredictionClient(HttpClient http) => _http = http;
    
    public async Task<PredictionResponse?> PredictAsync(Stream fileStream, string filename, string? contentType = null)
    {
        using var form = new MultipartFormDataContent();

        var fileContent = new StreamContent(fileStream);
        fileContent.Headers.ContentType = new MediaTypeHeaderValue(contentType ?? "image/jpeg"); 

        form.Add(fileContent, "image", filename);

        using var response = await _http.PostAsync(ApiUrl, form);
        response.EnsureSuccessStatusCode();

        var raw = await response.Content.ReadAsStringAsync();
        Console.WriteLine(raw);

        return await response.Content.ReadFromJsonAsync<PredictionResponse>(); 
    }
}