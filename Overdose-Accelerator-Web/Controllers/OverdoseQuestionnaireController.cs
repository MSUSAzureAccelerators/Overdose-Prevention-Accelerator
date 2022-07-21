using Microsoft.AspNetCore.Mvc;
using OverdoseAcceleratorWeb.Models;
using Newtonsoft.Json;
using System.Text;
using Microsoft.Extensions.Options;
using NuGet.Protocol;

namespace OverdoseWebAccelerator.Controllers
{
    public class OverdoseQuestionnaireController : Controller
    {
        private readonly ILogger<OverdoseQuestionnaireController> _logger;
        private readonly FormDictionaries _formDictionaries;
        private readonly WebServiceUrl _webservice; 

        public OverdoseQuestionnaireController(IOptions<FormDictionaries> formDictionaries, IOptions<WebServiceUrl> webservice,  ILogger<OverdoseQuestionnaireController> logger)
        {
            _logger = logger;
            _formDictionaries = formDictionaries.Value;
            _webservice = webservice.Value;
        }
        [HttpGet]
        public IActionResult Index()
        {
            var questionnaire = new QuestionnaireModel();
            questionnaire.LoadDictionaries(_formDictionaries);
            return View(questionnaire);
        }

        [HttpPost]
        public async Task<IActionResult> Results(QuestionnaireModel model)
        {
            var overdoseResult = new OverdoseResult(); 
            
            try
            {
                var url = _webservice.url + _webservice.token;
                var json = JsonConvert.SerializeObject(model.Questionnaire);
                var client = new HttpClient();
                var content = new StringContent(json, Encoding.UTF8, "application/json");
                var result = await client.PostAsync(url, content);
                if (result.IsSuccessStatusCode)
                {
                    if (result.Content is object) 
                    {
                        try
                        {
                            var resultStr = await result.Content.ReadAsStringAsync(); 
                            overdoseResult = JsonConvert.DeserializeObject<OverdoseResult>(resultStr);
                        }
                        catch (JsonReaderException)
                        {
                            _logger.LogError("Invalid JSON.");
                        }
                    }
                    else
                        _logger.LogError("HTTP Response was invalid and cannot be serialized.");
                }   
                else
                  _logger.LogError("The web service did not return a successful return.");
            }
            catch (Exception e)
            {
                _logger.LogError("There was an error trying to get information from the web service" + e.Message);
                throw;
            }

            return View(overdoseResult); 
        }
    }
}   
