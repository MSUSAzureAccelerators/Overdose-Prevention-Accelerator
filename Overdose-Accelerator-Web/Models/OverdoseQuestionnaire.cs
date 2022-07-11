namespace OverdoseAcceleratorWeb.Models
{
    public class OverdoseQuestionnaire
    {
        public int Education { get; set; }
        public int Age { get; set; }
        public string? Gender { get; set; }
        // Ever Drink Alcohol
        public bool EverAlcohol { get; set; }
        // Age at first use of alcohol
        public int AgeFirstAlcohol { get; set; }
        // Most resent use of alcohol
        public int RecentAlcohol { get; set; }
        // Days using alcohol last year
        public int DaysAlcoholUseYear { get; set; }
        // Have you ever had 4/5 or more drinks on the same occasion?
        public bool MoreDrinks { get; set; }
        // Have you had alcohol or drug use treatment in the past year?
        public bool HadTreatmentPastYear { get; set; }
        // Have you ever had alcohol or drug use treatment in your life?
        public bool HadTreatment { get; set; }
        // Ever Smoked Cigarettes
        public bool EverSmoked { get; set; }
        // Most recent use of cigarettes
        public int RecentCigarettes { get; set; }
        // Age when individual began smoking daily
        public int AgeFirstDailySmoke { get; set; }
        // First use of cigarettes prior to 18?
        public int AgeFirstSmoke { get; set; }
        // Have you used any tobacco product in the past year
        public bool TobaccoPastYear { get; set; }
        //Ever Cannabis Use 
        public bool EverCannabis { get; set; }
        // Most recent use of cannabis
        public int RecentCannabis { get; set; }
        // Days using cannabis in the past year
        public int DaysCannabisPastYear { get; set; }
        // First use of cannabis prior to 18?
        public int FirstCannabisUse { get; set; }
        // Ever Other Drugs
        public bool EverOther { get; set; }
        // Most recent use of cocaine
        public int RecentCocaine { get; set; }
        // Most recent use of crack cocaine
        public int RecentCrack { get; set; }
        public int RecentHeroin { get; set; }
        // Most recent use of hallucinogens
        public int RecentHallucinogens { get; set; }
        // Most recent use of LSD
        public int RecentLSD { get; set; }
        // Most recent use of Ectasy
        public int RecentEctasy { get; set; }
        // Most recent use of inhalants
        public int RecentInhalents { get; set; }
        // Most recent use of methamphetamine
        public int RecentMeth { get; set; }
        // Have you felt sad, empty, or depressed for several days or longer?
        public bool Depressed { get; set; }
        // Have you felt discouraged about life for several days or longer?
        public bool Discouraged { get; set; }
        // Have you ever been arrested and booked in the criminal justice system?
        public bool Arrested { get; set; }
    }
}
