namespace OverdoseAcceleratorWeb.Models
{
    public class OverdoseResult
    {
        public double score { get; set; }
        public double percentile { get; set; }

        public Dictionary<string, string>? features { get; set; }
    }
}
