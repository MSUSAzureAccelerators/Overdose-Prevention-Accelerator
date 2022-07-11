
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.Extensions.Options;

namespace OverdoseAcceleratorWeb.Models
{
    public class QuestionnaireModel 
    {
        public OverdoseQuestionnaire Questionnaire { get; set; }
        public IDictionary<string, string>? EducationLevels { get; set; }
        public IDictionary<string, string>? Ages { get; set; }

        public IDictionary<string, string>? RecentAlcohol { get; set; }
        public IDictionary<string, string>? RecentCig { get; set; }
        public IDictionary<string, string>? RecentPot { get; set; }
        public IDictionary<string, string>? RecentCocaine { get; set; }
        public IDictionary<string, string>? RecentCrack { get; set; }
        public IDictionary<string, string>? RecentHallucin { get; set; }
        public IDictionary<string, string>? RecentLSD { get; set; }
        public IDictionary<string, string>? RecentX { get; set; }
        public IDictionary<string, string>? RecentInhale { get; set; }
        public IDictionary<string, string>? RecentMeth { get; set; }

        public QuestionnaireModel()
        {
            Questionnaire = new OverdoseQuestionnaire();
        }

        public void LoadDictionaries(FormDictionaries dictionaries)
        {
            EducationLevels = dictionaries.Eduhighcat_dict;
            Ages = dictionaries.Age2_dict;
            RecentAlcohol = dictionaries.Iralcrc_dict;
            RecentCig = dictionaries.Ircigrc_dict;
            RecentPot = dictionaries.Irmjrc_dict;
            RecentCocaine = dictionaries.Ircocrc_dict;
            RecentCrack = dictionaries.Ircrkrc_dict;
            RecentHallucin = dictionaries.Irhallucrec_dict;
            RecentLSD = dictionaries.Irlsdrc_dict;
            RecentX = dictionaries.Irecstmorec_dict;
            RecentInhale = dictionaries.Irinhalrec_dict;
            RecentMeth = dictionaries.Irmethamrec_dict;

        }
    }
}
