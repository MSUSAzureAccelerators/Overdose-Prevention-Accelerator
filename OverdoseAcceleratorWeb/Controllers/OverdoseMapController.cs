using Microsoft.AspNetCore.Mvc;

namespace OverdoseAcceleratorWeb.Controllers
{
    public class OverdoseMapController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}
