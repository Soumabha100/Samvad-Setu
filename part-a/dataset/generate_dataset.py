import csv
import random
from collections import Counter

from pathlib import Path

random.seed(42)

OUTPUT_FILE = Path(__file__).resolve().parent / "complaints.csv"
TARGET_ROWS = 20000


# ============================================================
# LANGUAGES
# ============================================================

LANGUAGES = [
    "en",          # English
    "hi",          # Hindi
    "bn",          # Bengali
    "hinglish",    # Hindi + English
    "sat",         # Santali
    "nagpuri",     # Nagpuri / Sadri
    "mun",         # Mundari
    "kru",         # Kurukh / Oraon
    "ho"           # Ho
]


LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "bn": "Bengali",
    "hinglish": "Hinglish",
    "sat": "Santali",
    "nagpuri": "Nagpuri/Sadri",
    "mun": "Mundari",
    "kru": "Kurukh/Oraon",
    "ho": "Ho"
}


# ============================================================
# LOCATIONS
# ============================================================

LOCATIONS = {
    "en": [
        "near the school",
        "near the market",
        "near the railway station",
        "near the bus stand",
        "in our locality",
        "on the main road",
        "near the hospital",
        "in the residential area",
        "near the community center",
        "at the village entrance"
    ],

    "hi": [
        "स्कूल के पास",
        "बाजार के पास",
        "रेलवे स्टेशन के पास",
        "बस स्टैंड के पास",
        "हमारे इलाके में",
        "मुख्य सड़क पर",
        "अस्पताल के पास",
        "रिहायशी इलाके में",
        "सामुदायिक केंद्र के पास",
        "गांव के प्रवेश द्वार पर"
    ],

    "bn": [
        "স্কুলের কাছে",
        "বাজারের কাছে",
        "রেলস্টেশনের কাছে",
        "বাসস্ট্যান্ডের কাছে",
        "আমাদের এলাকায়",
        "প্রধান রাস্তায়",
        "হাসপাতালের কাছে",
        "আবাসিক এলাকায়",
        "কমিউনিটি সেন্টারের কাছে",
        "গ্রামের প্রবেশপথে"
    ],

    "hinglish": [
        "school ke paas",
        "market ke paas",
        "railway station ke paas",
        "bus stand ke paas",
        "hamare area mein",
        "main road par",
        "hospital ke paas",
        "residential area mein",
        "community center ke paas",
        "gaon ke entrance par"
    ]
}


# ============================================================
# ENGLISH TEMPLATES
# ============================================================

TEMPLATES = {

    "road_damage": {
        "low": [
            "There is a small pothole {location}.",
            "The road surface is slightly damaged {location}.",
            "A few cracks are visible on the road {location}.",
            "The road needs minor repair {location}."
        ],
        "medium": [
            "There is a pothole on the road {location}.",
            "The road is badly damaged {location}.",
            "Several potholes have appeared {location}.",
            "The road surface has deteriorated {location}."
        ],
        "high": [
            "There is a very large pothole blocking part of the road {location}.",
            "The road is severely damaged and vehicles are struggling to pass {location}.",
            "Multiple deep potholes are making the road dangerous {location}.",
            "The damaged road is causing traffic problems {location}."
        ],
        "critical": [
            "A huge pothole has made the road extremely dangerous {location}.",
            "The road has collapsed and vehicles cannot safely pass {location}.",
            "The road damage has already caused an accident {location}.",
            "The main road is completely unsafe because of severe damage {location}."
        ]
    },

    "garbage": {
        "low": [
            "A small amount of garbage is lying {location}.",
            "There is some litter {location}.",
            "A few waste items are lying on the roadside {location}.",
            "Some garbage needs to be collected {location}."
        ],
        "medium": [
            "The community dustbin is full and waste is spilling out {location}.",
            "The public waste container is overflowing onto the pavement {location}.",
            "A broken dustbin is spilling garbage onto the footpath {location}.",
            "Garbage is scattered across the street {location}.",
            "Waste has been piling up {location}.",
            "The garbage has not been collected {location}.",
            "There is a large amount of waste {location}."
        ],
        "high": [
            "A huge pile of garbage is blocking the road {location}.",
            "Garbage is overflowing and creating a serious problem {location}.",
            "Waste is blocking the drainage system {location}.",
            "The garbage dump is causing severe problems for residents {location}."
        ],
        "critical": [
            "A massive garbage dump is creating an immediate health hazard {location}.",
            "Burning garbage is producing dangerous smoke {location}.",
            "The garbage situation has become an emergency for nearby residents {location}.",
            "Waste is completely blocking access to the area {location}."
        ]
    },

    "drainage": {
        "low": [
            "There is a minor drainage problem {location}.",
            "The drain needs cleaning {location}.",
            "Water is draining slowly {location}.",
            "The drainage system needs attention {location}."
        ],
        "medium": [
            "The drain is partially blocked {location}.",
            "The drainage system is overflowing {location}.",
            "Dirty water is collecting near the drain {location}.",
            "The drain has not been cleaned for several days {location}."
        ],
        "high": [
            "The drainage system is completely blocked {location}.",
            "Blocked drains are flooding the street {location}.",
            "Sewage water is overflowing onto the road {location}.",
            "The blocked drain is causing serious problems {location}."
        ],
        "critical": [
            "An open manhole on the road has no cover creating a fatal risk {location}.",
            "The sewer manhole cover is missing on the street exposing a deep pit {location}.",
            "An open drain with missing lid is extremely dangerous {location}.",
            "Sewage is overflowing into homes {location}.",
            "The drainage failure has created a major health emergency {location}.",
            "Contaminated water is spreading through the neighborhood {location}.",
            "The drainage system has completely failed and residents are at risk {location}."
        ]
    },

    "waterlogging": {
        "low": [
            "There is some waterlogging {location}.",
            "A small amount of water has collected on the road {location}.",
            "Rainwater is standing on the street {location}."
        ],
        "medium": [
            "Water has accumulated across the road {location}.",
            "The street is partially waterlogged {location}.",
            "Heavy rain has caused waterlogging {location}."
        ],
        "high": [
            "Deep water is covering the road {location}.",
            "Waterlogging is preventing vehicles from passing {location}.",
            "The entire street is heavily waterlogged {location}."
        ],
        "critical": [
            "Severe waterlogging has trapped residents {location}.",
            "Floodwater has entered several houses {location}.",
            "People are unable to leave the area because of deep water {location}."
        ]
    },

    "flood": {
        "low": [
            "There is minor flooding near the road {location}.",
            "Water levels have started rising {location}.",
            "Some areas are affected by flooding {location}."
        ],
        "medium": [
            "Floodwater is spreading through the area {location}.",
            "The locality is experiencing flooding {location}.",
            "Floodwater has covered the streets {location}."
        ],
        "high": [
            "Severe flooding has affected the entire locality {location}.",
            "Floodwater has entered several buildings {location}.",
            "People are struggling to move because of flooding {location}."
        ],
        "critical": [
            "A major flood has trapped people in their homes {location}.",
            "The flood is threatening lives {location}.",
            "Residents urgently need rescue because of severe flooding {location}.",
            "Floodwater has reached dangerous levels {location}."
        ]
    },

    "building_damage": {
        "low": [
            "There is a small crack in a building wall {location}.",
            "Minor damage is visible on the building {location}.",
            "The building needs a safety inspection {location}."
        ],
        "medium": [
            "A large crack has appeared in the building {location}.",
            "Part of the building wall is damaged {location}.",
            "The building structure appears unsafe {location}."
        ],
        "high": [
            "A large section of the building has been damaged {location}.",
            "Part of the building has collapsed {location}.",
            "The damaged building is dangerous for people nearby {location}."
        ],
        "critical": [
            "The building has partially collapsed and people may be trapped {location}.",
            "A building has completely collapsed {location}.",
            "The collapsed building is creating an immediate danger to residents {location}."
        ]
    },

    "landslide": {
        "low": [
            "There is a small landslide near the road {location}.",
            "Some soil has fallen onto the roadside {location}."
        ],
        "medium": [
            "A landslide has covered part of the road {location}.",
            "Mud and rocks are blocking part of the road {location}."
        ],
        "high": [
            "A large landslide has blocked the road {location}.",
            "Heavy debris is covering the road {location}.",
            "The landslide is making travel dangerous {location}."
        ],
        "critical": [
            "A massive landslide has completely blocked the road {location}.",
            "People may be trapped because of the landslide {location}.",
            "The landslide has damaged homes and is threatening lives {location}."
        ]
    },

    "bridge_damage": {
        "low": [
            "There is minor damage on the bridge {location}.",
            "The bridge needs inspection {location}."
        ],
        "medium": [
            "The bridge railing is damaged {location}.",
            "Part of the bridge is damaged {location}."
        ],
        "high": [
            "The bridge is severely damaged and unsafe {location}.",
            "Vehicles are having difficulty crossing the damaged bridge {location}."
        ],
        "critical": [
            "The bridge is collapsing and people are in immediate danger {location}.",
            "The bridge has become completely unsafe for traffic {location}.",
            "A section of the bridge has collapsed {location}."
        ]
    },

    "fire": {
        "low": [
            "There is a small fire {location}.",
            "Smoke is coming from a building {location}."
        ],
        "medium": [
            "A fire has started {location}.",
            "The fire is spreading near the roadside {location}."
        ],
        "high": [
            "A large fire is spreading quickly {location}.",
            "The fire is threatening nearby buildings {location}."
        ],
        "critical": [
            "A major fire is threatening people's lives {location}.",
            "People are trapped inside a burning building {location}.",
            "The fire has spread across multiple buildings {location}."
        ]
    },

    "water_supply": {
        "low": [
            "The water supply is slightly irregular {location}.",
            "There is a minor water supply issue {location}."
        ],
        "medium": [
            "There has been no water supply since morning {location}.",
            "The water supply has been interrupted {location}.",
            "Residents are facing water shortages {location}."
        ],
        "high": [
            "There has been no drinking water for several days {location}.",
            "The water supply has completely stopped {location}.",
            "Residents urgently need drinking water {location}."
        ],
        "critical": [
            "The entire locality has no safe drinking water {location}.",
            "A water supply failure is putting residents at serious risk {location}."
        ]
    },

    "other": {
        "low": [
            "There is a civic issue that needs attention {location}.",
            "Please inspect the public area {location}."
        ],
        "medium": [
            "There is a public infrastructure problem {location}.",
            "Residents are facing a civic problem {location}."
        ],
        "high": [
            "The traffic light signal is not working at the intersection creating accident danger {location}.",
            "Stray cattle and cows are blocking the active roadway {location}.",
            "The traffic signal is broken and dead at the crossroads {location}.",
            "Stray animals wandering on the highway are endangering drivers {location}.",
            "A serious civic problem is affecting residents {location}.",
            "The issue is causing major disruption {location}."
        ],
        "critical": [
            "There is an emergency situation requiring immediate assistance {location}.",
            "Residents are facing an immediate safety risk {location}."
        ]
    }
}


# ============================================================
# HINDI TEMPLATES
# ============================================================

HINDI_TEMPLATES = {
    "road_damage": {
        "low": [
            "सड़क पर छोटा सा गड्ढा बन गया है {location}।",
            "सड़क की सतह पर हल्की दरारें दिखाई दे रही हैं {location}।",
            "सड़क की हल्की मरम्मत की आवश्यकता है {location}।",
            "सड़क पर थोड़ा नुकसान हुआ है {location}।"
        ],
        "medium": [
            "सड़क पर गड्ढा है {location}।",
            "सड़क काफी खराब हो गई है {location}।",
            "सड़क पर कई गड्ढे बन गए हैं {location}।",
            "सड़क की हालत खराब हो रही है {location}।"
        ],
        "high": [
            "सड़क पर बड़ा और गहरा गड्ढा है जिससे गाड़ियाँ नहीं निकल पा रही हैं {location}।",
            "सड़क बहुत ज्यादा क्षतिग्रस्त है और यातायात बाधित हो रहा है {location}।",
            "गहरे गड्ढों के कारण सड़क पर भारी जाम लग रहा है {location}।",
            "सड़क की गंभीर खराबी से कभी भी हादसा हो सकता है {location}।"
        ],
        "critical": [
            "सड़क धंस गई है और आवाजाही पूरी तरह खतरनाक हो चुकी है {location}।",
            "सड़क के बड़े गड्ढे के कारण गंभीर दुर्घटना हो गई है {location}।",
            "मुख्य सड़क पूरी तरह टूटकर बंद हो गई है, आपातकालीन खतरा है {location}।",
            "सड़क पूरी तरह धंसने से लोगों की जान को भारी खतरा है {location}।"
        ]
    },
    "garbage": {
        "low": [
            "सड़क किनारे थोड़ा सा कचरा पड़ा हुआ है {location}।",
            "यहाँ थोड़ा कूड़ा जमा है {location}।",
            "कचरे की हल्की सफाई की जरूरत है {location}।",
            "कुछ सूखा कचरा पड़ा हुआ है {location}।"
        ],
        "medium": [
            "कचरे का डस्टबिन और वेस्ट कंटेनर भरकर सड़क पर फैल रहा है {location}।",
            "सार्वजनिक कूड़ेदान ओवरफ्लो हो गया है और बदबू फैल रही है {location}।",
            "सड़क पर काफी कचरा बिखरा हुआ है {location}।",
            "कचरे का ढेर लग गया है और बदबू आ रही है {location}।",
            "कई दिनों से कचरा नहीं उठाया गया है {location}।",
            "कूड़ा जमा होने से लोगों को परेशानी हो रही है {location}।"
        ],
        "high": [
            "कचरे का भारी ढेर पूरी सड़क रोक रहा है {location}।",
            "सड़े हुए कचरे से बीमारियाँ फैलने का गंभीर खतरा पैदा हो गया है {location}।",
            "कचरे के बड़े ढेर से नाली पूरी तरह जाम हो गई है {location}।",
            "कूड़े के भयानक अंबार से पूरा इलाका परेशान है {location}।"
        ],
        "critical": [
            "कचरे के विशाल ढेर में जहरीला धुआं और आग लग गई है {location}।",
            "कचरे के कारण गंभीर महामारी फैलने का आपातकालीन संकट है {location}।",
            "सड़ते हुए कचरे और मेडिकल वेस्ट से जानलेवा स्थिति बन गई है {location}।",
            "कचरे के भारी ढेर से रास्ता पूरी तरह बंद और लोगों का दम घुट रहा है {location}।"
        ]
    },
    "drainage": {
        "low": [
            "नाली से पानी थोड़ा धीरे निकल रहा है {location}।",
            "नाली की हल्की सफाई की आवश्यकता है {location}।",
            "नाली में थोड़ा कचरा फंसा हुआ है {location}।",
            "जल निकासी में थोड़ी रुकावट है {location}।"
        ],
        "medium": [
            "नाली आंशिक रूप से बंद हो गई है {location}।",
            "नाली का गंदा पानी सड़क पर आ रहा है {location}।",
            "नाली कई दिनों से साफ नहीं हुई है और बदबू फैल रही है {location}।",
            "नाली का पानी ओवरफ्लो कर रहा है {location}।"
        ],
        "high": [
            "नाली पूरी तरह से चोक हो गई है और सीवर का पानी बह रहा है {location}।",
            "गंदा सीवेज पानी पूरे रास्ते पर भर गया है {location}।",
            "नाली बंद होने से भारी जलजमाव और संक्रमण का खतरा है {location}।",
            "ड्रेनेज सिस्टम पूरी तरह ठप हो गया है {location}।"
        ],
        "critical": [
            "सड़क पर खुला मैनहोल पड़ा है जिसका ढक्कन गायब है जानलेवा खतरा {location}।",
            "खुले नाले और मैनहोल से किसी की जान जा सकती है तुरंत ढक्कन लगाएं {location}।",
            "सीवर और नाली का दूषित पानी लोगों के घरों में घुस गया है {location}।",
            "नाली टूटने से घरों में जहरीला पानी भर रहा है, गंभीर स्वास्थ्य संकट {location}।",
            "सीवेज के दूषित पानी से बच्चों और परिवारों की जान खतरे में है {location}।",
            "ड्रेनेज लाइन फटने से भीषण आपदा जैसी स्थिति बन गई है {location}।"
        ]
    },
    "waterlogging": {
        "low": [
            "सड़क पर थोड़ा पानी जमा हुआ है {location}।",
            "बारिश के बाद हल्का पानी भर गया है {location}।",
            "सड़क के किनारे हल्का जलभराव है {location}।"
        ],
        "medium": [
            "सड़क पर काफी पानी भर गया है {location}।",
            "बारिश के कारण रास्ता जलमग्न हो गया है {location}।",
            "जलभराव की वजह से पैदल चलने में दिक्कत हो रही है {location}।"
        ],
        "high": [
            "सड़क पर गहरा पानी भर गया है और गाड़ियाँ बंद पड़ रही हैं {location}।",
            "भारी जलभराव के कारण पूरा मुख्य मार्ग बंद हो चुका है {location}।",
            "गहरे पानी में दोपहिया और पैदल यात्री गिर रहे हैं {location}।"
        ],
        "critical": [
            "भीषण जलभराव से लोग अपने घरों में फंसे हुए हैं {location}।",
            "बाढ़ जैसा पानी घरों और दुकानों में घुस गया है, बचाव कार्य जरूरी {location}।",
            "जलभराव इतना गहरा है कि डूबने का खतरा बन चुका है {location}।"
        ]
    },
    "flood": {
        "low": [
            "नदी या नाले का जलस्तर थोड़ा बढ़ रहा है {location}।",
            "निचले इलाके में पानी का स्तर हल्का बढ़ा है {location}।",
            "बाढ़ का थोड़ा सा पानी सड़क किनारे दिखाई दे रहा है {location}।"
        ],
        "medium": [
            "इलाके में बाढ़ का पानी फैलने लगा है {location}।",
            "बाढ़ का पानी मुख्य रास्तों पर आ गया है {location}।",
            "क्षेत्र में बाढ़ की स्थिति बनती जा रही है {location}।"
        ],
        "high": [
            "गंभीर बाढ़ से पूरा इलाका डूब गया है {location}।",
            "बाढ़ का पानी कई इमारतों और दुकानों में घुस चुका है {location}।",
            "लोग बाढ़ के पानी में फंस गए हैं और सुरक्षित स्थान ढूंढ रहे हैं {location}।"
        ],
        "critical": [
            "भीषण बाढ़ में लोग अपने घरों की छतों पर फंसे हैं, तुरंत नाव और बचाव चाहिए {location}।",
            "प्रलयंकारी बाढ़ से जान-माल का भारी खतरा है, तत्काल रेस्क्यू टीम भेजें {location}।",
            "बाढ़ के तेज बहाव में लोग बहने की कगार पर हैं, जान का भारी जोखिम है {location}।"
        ]
    },
    "building_damage": {
        "low": [
            "इमारत की बाहरी दीवार पर छोटी दरार आ गई है {location}।",
            "इमारत पर मामूली क्षति नजर आ रही है {location}।",
            "भवन की सुरक्षा जांच की जरूरत है {location}।"
        ],
        "medium": [
            "इमारत की दीवार में बड़ी दरार पड़ गई है {location}।",
            "इमारत का एक हिस्सा जर्जर होकर गिर रहा है {location}।",
            "भवन की संरचना कमजोर और असुरक्षित दिख रही है {location}।"
        ],
        "high": [
            "इमारत का बड़ा हिस्सा क्षतिग्रस्त हो गया है और कभी भी गिर सकता है {location}।",
            "जर्जर इमारत से प्लास्टर और ईंटें नीचे गिर रही हैं, बहुत खतरनाक {location}।",
            "इमारत की बालकनी टूटकर गिर चुकी है, बड़ा हादसा हो सकता है {location}।"
        ],
        "critical": [
            "इमारत भरभराकर गिर गई है और मलबे में लोग दबे हो सकते हैं {location}।",
            "पूरी इमारत ढह गई है, तुरंत राहत और बचाव कार्य की आवश्यकता है {location}।",
            "इमारत पूरी तरह ध्वस्त होने से कई जिंदगियां खतरे में हैं {location}।"
        ]
    },
    "landslide": {
        "low": [
            "पहाड़ी से थोड़ी मिट्टी और छोटे कंकड़ सड़क पर गिरे हैं {location}।",
            "हल्का भूस्खलन हुआ है पर आवाजाही जारी है {location}।"
        ],
        "medium": [
            "भूस्खलन के कारण सड़क का एक हिस्सा बंद हो गया है {location}।",
            "मलबा और पत्थर सड़क पर आ गए हैं {location}।"
        ],
        "high": [
            "बड़ा भूस्खलन होने से पूरा रास्ता बंद हो गया है {location}।",
            "सड़क पर भारी चट्टानें और मलबा जमा है, यात्रा खतरनाक {location}।"
        ],
        "critical": [
            "भीषण भूस्खलन से कई वाहन और लोग मलबे में दब गए हैं, तुरंत रेस्क्यू चाहिए {location}।",
            "विशाल भूस्खलन ने घरों को तबाह कर दिया है, लोगों की जान संकट में है {location}।"
        ]
    },
    "bridge_damage": {
        "low": [
            "पुल की सतह पर मामूली दरार दिख रही है {location}।",
            "पुल के किनारे थोड़ी मरम्मत की जरूरत है {location}।"
        ],
        "medium": [
            "पुल की रेलिंग टूट गई है {location}।",
            "पुल का एक हिस्सा क्षतिग्रस्त नजर आ रहा है {location}।"
        ],
        "high": [
            "पुल में गहरी दरारें आ गई हैं और भारी वाहनों के लिए असुरक्षित है {location}।",
            "पुल का पिलर कमजोर हो गया है, कभी भी गिर सकता है {location}।"
        ],
        "critical": [
            "पुल टूटकर नदी में गिर गया है और आवागमन पूरी तरह ध्वस्त हो गया है {location}।",
            "पुल का बड़ा हिस्सा ढह गया है और कई लोग संकट में हैं {location}।"
        ]
    },
    "fire": {
        "low": [
            "कचरे के छोटे ढेर में हल्की आग लगी है {location}।",
            "सड़क किनारे थोड़ा धुआं उठता दिख रहा है {location}।"
        ],
        "medium": [
            "यहाँ आग लग गई है और फैल रही है {location}।",
            "झाड़ियों में आग भड़क रही है {location}।"
        ],
        "high": [
            "इमारत में भीषण आग फैल रही है और ऊंची लपटें उठ रही हैं {location}।",
            "आग आसपास के घरों और दुकानों की तरफ तेजी से बढ़ रही है {location}।"
        ],
        "critical": [
            "आग की लपटों में लोग घर के अंदर फंसे हुए हैं, तुरंत दमकल भेजें जान का खतरा है {location}।",
            "भीषण आग में कई घर जल रहे हैं और कई लोग जलने के खतरे में हैं {location}।"
        ]
    },
    "water_supply": {
        "low": [
            "पानी का दबाव थोड़ा कम आ रहा है {location}।",
            "आज पानी की सप्लाई थोड़ी देर से आई {location}।"
        ],
        "medium": [
            "सुबह से पानी की सप्लाई पूरी तरह बंद है {location}।",
            "नलों में गंदा पानी आ रहा है {location}।"
        ],
        "high": [
            "पिछले चार दिनों से पीने का एक बूंद पानी नहीं आया है {location}।",
            "पानी की मुख्य पाइपलाइन फट गई है और पूरा इलाका प्यासा है {location}।"
        ],
        "critical": [
            "पीने के पानी में सीवेज का जहरीला पानी मिल गया है, लोग गंभीर बीमार पड़ रहे हैं {location}।",
            "पानी की सप्लाई में विषैला केमिकल आने से कई लोग अस्पताल पहुंच गए हैं {location}।"
        ]
    },
    "other": {
        "low": [
            "यहाँ एक सामान्य नागरिक समस्या है जिस पर ध्यान देने की जरूरत है {location}।",
            "क्षेत्र का सामान्य निरीक्षण करने का अनुरोध है {location}।"
        ],
        "medium": [
            "सार्वजनिक सुविधा में खराबी के कारण लोगों को असुविधा हो रही है {location}।",
            "इलाके में नागरिक व्यवस्था प्रभावित है {location}।"
        ],
        "high": [
            "चौराहे पर ट्रैफिक लाइट खराब है और सिग्नल बंद पड़ा है {location}।",
            "सड़क पर आवारा मवेशी और गायें बैठी हैं जिससे जाम लग रहा है {location}।",
            "ट्रैफिक सिग्नल बंद होने से चौराहे पर कभी भी एक्सीडेंट हो सकता है {location}।",
            "सड़क पर आवारा पशुओं के आतंक से लोग सुरक्षित नहीं हैं {location}।",
            "एक गंभीर नागरिक समस्या से पूरा मोहल्ला परेशान और आक्रोशित है {location}।",
            "समस्या से दैनिक जनजीवन पूरी तरह ठप हो गया है {location}।"
        ],
        "critical": [
            "अत्यंत गंभीर आपातकालीन स्थिति उत्पन्न हो गई है, तुरंत सरकारी मदद चाहिए {location}।",
            "गंभीर सार्वजनिक संकट से लोगों की सुरक्षा को सीधा खतरा है {location}।"
        ]
    }
}


# ============================================================
# BENGALI TEMPLATES
# ============================================================

BENGALI_TEMPLATES = {
    "road_damage": {
        "low": [
            "রাস্তায় সামান্য একটি গর্ত হয়েছে {location}।",
            "রাস্তার উপরিভাগে ছোট ফাটল দেখা দিয়েছে {location}।",
            "রাস্তাটিতে হালকা মেরামতের প্রয়োজন {location}।",
            "রাস্তায় সামান্য ক্ষতি হয়েছে {location}।"
        ],
        "medium": [
            "রাস্তায় গর্ত হয়েছে এবং চলাচলে অসুবিধা হচ্ছে {location}।",
            "রাস্তার অবস্থা বেশ খারাপ হয়ে গেছে {location}।",
            "রাস্তায় কয়েকটি গর্ত সৃষ্টি হয়েছে {location}।",
            "রাস্তার বেহাল দশা দ্রুত মেরামত দরকার {location}।"
        ],
        "high": [
            "রাস্তায় বিশাল গভীর গর্তের কারণে যানবাহন চলাচল বন্ধ {location}।",
            "রাস্তা মারাত্মক ক্ষতিগ্রস্ত হয়েছে এবং ভয়াবহ যানজট সৃষ্টি হচ্ছে {location}।",
            "গভীর খানাখন্দের কারণে প্রায়ই দুর্ঘটনা ঘটছে {location}।",
            "ক্ষতিগ্রস্ত রাস্তায় যেকোনো সময় বড় বিপদ ঘটতে পারে {location}।"
        ],
        "critical": [
            "প্রধান রাস্তা ধসে গিয়ে ভয়াবহ পরিস্থিতি তৈরি হয়েছে {location}।",
            "রাস্তা ভেঙে পড়ে ইতিমধ্যেই মারাত্মক দুর্ঘটনা ঘটেছে, জীবন বিপন্ন {location}।",
            "রাস্তা সম্পূর্ণ দেবে গিয়ে চলাচল একেবারেই বন্ধ, জরুরি হস্তক্ষেপ চাই {location}।",
            "রাস্তা ধসে মানুষের প্রাণহানির চরম আশঙ্কা তৈরি হয়েছে {location}।"
        ]
    },
    "garbage": {
        "low": [
            "রাস্তার পাশে অল্প কিছু আবর্জনা পড়ে আছে {location}।",
            "এখানে সামান্য কিছু নোংরা জমেছে {location}।",
            "কিছু বর্জ্য পদার্থ পড়ে রয়েছে {location}।",
            "সামান্য আবর্জনা পরিষ্কার করা দরকার {location}।"
        ],
        "medium": [
            "রাস্তায় আবর্জনা পড়ে আছে এবং দুর্গন্ধ ছড়াচ্ছে {location}।",
            "আবর্জনার স্তূপ জমে গেছে {location}।",
            "কয়েকদিন ধরে আবর্জনা পরিষ্কার করা হয়নি {location}।",
            "আবর্জনার কারণে মানুষের স্বাভাবিক চলাচলে সমস্যা হচ্ছে {location}।"
        ],
        "high": [
            "বিশাল আবর্জনার স্তূপ পুরো রাস্তা আটকে দিয়েছে {location}।",
            "পচা আবর্জনা উপচে পড়ে সংক্রামক ব্যাধি ছড়ানোর মারাত্মক ঝুঁকি {location}।",
            "আবর্জনার স্তূপ নর্দমা বন্ধ করে গুরুতর সমস্যা সৃষ্টি করেছে {location}।",
            "আবর্জনার পচা গন্ধে আবাসিক এলাকা বসবাসের অযোগ্য হয়ে পড়েছে {location}।"
        ],
        "critical": [
            "আবর্জনার বিশাল ভাগাড়ে আগুন লেগে বিষাক্ত ধোঁয়ায় মানুষের দম বন্ধ হয়ে আসছে {location}।",
            "মেডিকেল বর্জ্য এবং ক্ষতিকর আবর্জনায় মারাত্মক স্বাস্থ্য বিপর্যয় {location}।",
            "আবর্জনা ধসে রাস্তা সম্পূর্ণ অবরুদ্ধ ও জরুরি অবস্থা তৈরি হয়েছে {location}।",
            "পচা বর্জ্যে মহামারীর চরম বিপদ, অবিলম্বে পরিষ্কার করুন {location}।"
        ]
    },
    "drainage": {
        "low": [
            "নর্দমা দিয়ে জল ধীরে নিষ্কাশন হচ্ছে {location}।",
            "ড্রেনটির সামান্য পরিষ্কার পরিচ্ছন্নতা প্রয়োজন {location}।",
            "নর্দমায় সামান্য ময়লা জমেছে {location}।",
            "ড্রেনেজ ব্যবস্থায় হালকা সমস্যা দেখা দিয়েছে {location}।"
        ],
        "medium": [
            "নর্দমা আংশিক বন্ধ হয়ে জল আটকে আছে {location}।",
            "নর্দমার নোংরা জল রাস্তায় উপচে পড়ছে {location}।",
            "কয়েকদিন ধরে ড্রেন পরিষ্কার না করায় দুর্গন্ধ ছড়াচ্ছে {location}।",
            "নর্দমা আটকে যাওয়ায় নিকাশি সমস্যা হচ্ছে {location}।"
        ],
        "high": [
            "নর্দমা সম্পূর্ণ বন্ধ হয়ে পুরো রাস্তা নর্দমার জলে ডুবে গেছে {location}।",
            "ড্রেন উপচে বিষাক্ত কালো জল রাস্তায় ভাসছে {location}।",
            "নর্দমা বিকল হওয়ায় ব্যাপক জলজট এবং রোগ ছড়াচ্ছে {location}।",
            "ড্রেনেজ ব্যবস্থা সম্পূর্ণরূপে ভেঙে পড়েছে {location}।"
        ],
        "critical": [
            "নর্দমার দূষিত মলমূত্র মিশ্রিত জল মানুষের ঘরের ভেতর ঢুকে গেছে {location}।",
            "নর্দমা ফেটে ঘরে নোংরা জল ঢুকে শিশুরা এবং বাসিন্দারা মারাত্মক বিপদে {location}।",
            "ড্রেন বিপর্যয়ে জনস্বাস্থ্যের জরুরি সংকট ও জীবন সংশয় তৈরি হয়েছে {location}।",
            "দূষিত নিকাশি জলে সমগ্র এলাকা প্লাবিত হয়ে চরম বিপর্যয় {location}।"
        ]
    },
    "waterlogging": {
        "low": [
            "রাস্তায় সামান্য জল জমে রয়েছে {location}।",
            "বৃষ্টির পর সামান্য জল জমেছে {location}।",
            "রাস্তার ধারে কিছুটা জল দাঁড়ানো {location}।"
        ],
        "medium": [
            "রাস্তায় বেশ জল জমে গেছে {location}।",
            "বৃষ্টির কারণে জলাবদ্ধতা সৃষ্টি হয়েছে {location}।",
            "জল জমে থাকায় চলাচলে অসুবিধা হচ্ছে {location}।"
        ],
        "high": [
            "কোমর সমান জল জমে রাস্তা সম্পূর্ণ অচল হয়ে গেছে {location}।",
            "ভারী জলমগ্নতার কারণে গাড়ি বিকল হয়ে যান চলাচল স্তব্ধ {location}।",
            "গভীর জলে পথচারী ও যাত্রীরা বারবার দুর্ঘটনার শিকার হচ্ছেন {location}।"
        ],
        "critical": [
            "ভয়াবহ জলজটে মানুষ বাড়িতে আটকা পড়েছে, পানিবন্দী অবস্থা {location}।",
            "জল ঘরের ভেতরে ঢুকে সম্পূর্ণ জীবনযাত্রা বিপন্ন করেছে {location}।",
            "জলে ডুবে যাওয়ার ঝুঁকি তৈরি হয়েছে, উদ্ধার তৎপরতা প্রয়োজন {location}।"
        ]
    },
    "flood": {
        "low": [
            "নদীর জল সামান্য বাড়তে শুরু করেছে {location}।",
            "নিচু এলাকায় সামান্য বন্যার জল দেখা যাচ্ছে {location}।",
            "রাস্তার পাশে সামান্য জল ঢুকছে {location}।"
        ],
        "medium": [
            "এলাকায় বন্যার জল ঢুকতে শুরু করেছে {location}।",
            "বন্যার জল রাস্তায় উপচে পড়ছে {location}।",
            "এলাকাটি প্লাবিত হওয়ার আশঙ্কা তৈরি হয়েছে {location}।"
        ],
        "high": [
            "গুরুতর বন্যায় পুরো এলাকা তলিয়ে গেছে {location}।",
            "বন্যার জল অনেক ঘরবাড়ি এবং দোকানে প্রবেশ করেছে {location}।",
            "মানুষ বন্যার কারণে গৃহহীন হয়ে পড়েছে {location}।"
        ],
        "critical": [
            "ভয়াবহ বন্যায় মানুষ ছাদের উপর আটকা পড়েছে, দ্রুত উদ্ধারকারী দল প্রয়োজন {location}।",
            "বন্যার তীব্র স্রোতে মানুষের প্রাণহানির জরুরি আশঙ্কা তৈরি হয়েছে {location}।",
            "বন্যার জল বিপদসীমার বহু উপরে উঠে জীবন চরম ঝুঁকিতে {location}।"
        ]
    },
    "building_damage": {
        "low": [
            "বিল্ডিংয়ের দেওয়ালে ছোট ফাটল দেখা দিয়েছে {location}।",
            "ভবনে সামান্য ক্ষয়ক্ষতি হয়েছে {location}।",
            "ভবনটির নিরাপত্তা পরীক্ষা করা উচিত {location}।"
        ],
        "medium": [
            "বিল্ডিংয়ের দেওয়ালে বড় ফাটল সৃষ্টি হয়েছে {location}।",
            "ভবনের একটি অংশ ভেঙে ক্ষয়ক্ষতি হচ্ছে {location}।",
            "বিল্ডিংটির অবস্থা ঝুঁকিপূর্ণ মনে হচ্ছে {location}।"
        ],
        "high": [
            "ভবনের একটি বড় অংশ ক্ষতিগ্রস্ত এবং যেকোনো মুহূর্তে ভেঙে পড়তে পারে {location}।",
            "বিপজ্জনক ভবন থেকে চাঙড় খসে পড়ছে {location}।",
            "ভবনটির কাঠামো মারাত্মক হেলে পড়েছে {location}।"
        ],
        "critical": [
            "বিল্ডিং ভেঙে পড়েছে এবং মানুষ ধ্বংসস্তূপে চাপা পড়ে আছে {location}।",
            "পুরো ভবন সম্পূর্ণ ধসে পড়েছে, জরুরি উদ্ধার কাজ শুরু করুন {location}।",
            "ভবন ধ্বসে মানুষের জীবন চরম বিপন্ন {location}।"
        ]
    },
    "landslide": {
        "low": [
            "পাহাড়ের গা থেকে সামান্য মাটি রাস্তায় পড়েছে {location}।",
            "ছোটখাটো ভূমিধস হয়েছে তবে রাস্তা সচল আছে {location}।"
        ],
        "medium": [
            "ভূমিধসের কারণে রাস্তার একপাশ আটকে গেছে {location}।",
            "পাথর এবং কাদা রাস্তায় এসে পড়েছে {location}।"
        ],
        "high": [
            "বিশাল ভূমিধসে রাস্তা সম্পূর্ণ অবরুদ্ধ হয়ে গেছে {location}।",
            "ভারী পাথরের কারণে যাতায়াত অত্যন্ত বিপজ্জনক {location}।"
        ],
        "critical": [
            "ভয়াবহ ভূমিধসে গাড়ি এবং মানুষ মাটির নিচে চাপা পড়েছে {location}।",
            "ভূমিধসে ঘরবাড়ি ধ্বংস হয়ে মানুষের প্রাণহানির চরম বিপদ {location}।"
        ]
    },
    "bridge_damage": {
        "low": [
            "সেতুতে সামান্য ফাটল দেখা গেছে {location}।",
            "সেতুটিতে ছোট মেরামতের প্রয়োজন {location}।"
        ],
        "medium": [
            "সেতুর রেলিং ভেঙে গেছে {location}।",
            "সেতুর একটি অংশ ক্ষতিগ্রস্ত হয়েছে {location}।"
        ],
        "high": [
            "সেতুতে বড় ফাটল ধরেছে এবং ভারী যানের জন্য মারাত্মক বিপজ্জনক {location}।",
            "সেতুর স্তম্ভ দুর্বল হয়ে পড়েছে {location}।"
        ],
        "critical": [
            "সেতু ভেঙে নদীতে পড়ে গেছে এবং চলাচল সম্পূর্ণ বিচ্ছিন্ন {location}।",
            "সেতু ধসে বহু মানুষ বিপদে পড়েছে, চরম বিপর্যয় {location}।"
        ]
    },
    "fire": {
        "low": [
            "ময়লার স্তূপে সামান্য আগুন লেগেছে {location}।",
            "রাস্তার পাশে ধোঁয়া দেখা যাচ্ছে {location}।"
        ],
        "medium": [
            "এখানে আগুন লেগেছে এবং চারদিকে ছড়াচ্ছে {location}।",
            "ঝোপঝাড়ে আগুন জ্বলছে {location}।"
        ],
        "high": [
            "বিল্ডিংয়ে ভয়াবহ আগুন লেগেছে এবং দ্রুত বিস্তার লাভ করছে {location}।",
            "আগুনের তীব্র শিখা আশেপাশের ঘরবাড়িতে পৌঁছানোর আশঙ্কা {location}।"
        ],
        "critical": [
            "আগুনে মানুষ ঘরের ভেতর আটকা পড়েছে, অবিলম্বে দমকল পাঠান জীবন বিপন্ন {location}।",
            "ভয়াবহ অগ্নিকাণ্ডে একাধিক বাড়ি পুড়ে যাচ্ছে, মানুষের জীবন ঝুঁকিতে {location}।"
        ]
    },
    "water_supply": {
        "low": [
            "জলের চাপ কিছুটা কম আসছে {location}।",
            "আজ জল সরবরাহে সামান্য বিলম্ব হয়েছে {location}।"
        ],
        "medium": [
            "সকাল থেকে জল সরবরাহ পুরোপুরি বন্ধ রয়েছে {location}।",
            "পাইপ থেকে ঘোলা ও ময়লা জল আসছে {location}।"
        ],
        "high": [
            "গত চারদিন ধরে পানীয় জলের সরবরাহ সম্পূর্ণ বন্ধ {location}।",
            "জলের মূল পাইপ ফেটে পুরো এলাকা জলের হাহাকারে ভুগছে {location}।"
        ],
        "critical": [
            "পানীয় জলের সাথে বিষাক্ত নর্দমার জল মিশে মানুষ ডায়রিয়ায় আক্রান্ত হচ্ছে {location}।",
            "বিষাক্ত জল সরবরাহের ফলে বহু মানুষ হাসপাতালে ভর্তি {location}।"
        ]
    },
    "other": {
        "low": [
            "এখানে একটি সাধারণ নাগরিক সমস্যা রয়েছে যা দেখা দরকার {location}।",
            "এলাকাটি একবার পরিদর্শন করার অনুরোধ রইল {location}।"
        ],
        "medium": [
            "জনসেবামূলক সমস্যায় মানুষ ভোগান্তিতে পড়েছে {location}।",
            "নাগরিক অসুবিধা দূর করতে আবেদন জানাচ্ছি {location}।"
        ],
        "high": [
            "গুরুতর নাগরিক সমস্যায় সমগ্র এলাকা ভীষণ ক্ষতিগ্রস্ত {location}।",
            "এই সমস্যার কারণে জনজীবন অচল হয়ে পড়েছে {location}।"
        ],
        "critical": [
            "একটি মারাত্মক জরুরি সংকট তৈরি হয়েছে, অবিলম্বে প্রশাসনিক সাহায্য চাই {location}।",
            "ভয়াবহ জননিরাপত্তাজনিত ঝুঁকি দেখা দিয়েছে {location}।"
        ]
    }
}


# ============================================================
# HINGLISH TEMPLATES
# ============================================================

HINGLISH_TEMPLATES = {
    "road_damage": {
        "low": [
            "Road pe chota sa pothole hai {location}.",
            "Sadak ki surface pe thoda damage dikh raha hai {location}.",
            "Road ko minor repair ki zaroorat hai {location}.",
            "Thoda sa road damage hai {location}."
        ],
        "medium": [
            "Road par bada pothole hai aur gaadi chalana mushkil ho raha hai {location}.",
            "Sadak kafi kharab ho chuki hai {location}.",
            "Road par multiple potholes ban gaye hain {location}.",
            "Sadak ki haalat kharab hai {location}."
        ],
        "high": [
            "Road par bahut deep aur dangerous potholes hain jisse traffic jam lag raha hai {location}.",
            "Road severely damaged ho chuki hai aur vehicles phas rahe hain {location}.",
            "Heavy damage ki wajah se road pe roz accidents ka risk hai {location}.",
            "Gahre gaddhe ki wajah se road block hone jaisi ho gayi hai {location}."
        ],
        "critical": [
            "Road completely collapse ho gayi hai aur already serious accident ho chuka hai {location}.",
            "Huge pit ki wajah se road totally collapse ho chuki hai, life threat situation {location}.",
            "Main road dhans gayi hai aur emergency vehicle bhi nahi nikal sakti {location}.",
            "Road completely destroy ho gayi hai, immediate danger hai {location}."
        ]
    },
    "garbage": {
        "low": [
            "Road side thoda sa garbage pada hai {location}.",
            "Yahan thoda litter jama ho gaya hai {location}.",
            "Kuch waste pada hai jise clean karna chahiye {location}.",
            "Halka phulka kachra jama hai {location}."
        ],
        "medium": [
            "Road par kafi garbage faila hua hai aur bad smell aa rahi hai {location}.",
            "Kachre ka dher jama ho gaya hai {location}.",
            "Kai din se garbage collect nahi kiya gaya {location}.",
            "Garbage ki wajah se aas-paas ke log pareshaan hain {location}."
        ],
        "high": [
            "Garbage ka massive pile poori road block kar raha hai {location}.",
            "Overflowing garbage se serious disease failne ka severe risk hai {location}.",
            "Kachre ke dher ne nali ko totally block kar diya hai {location}.",
            "Huge garbage dump se locality me severe problem ho gayi hai {location}."
        ],
        "critical": [
            "Huge garbage dump me aag lag gayi hai aur toxic smoke se dam ghut raha hai {location}.",
            "Medical waste aur rotten garbage se immediate health emergency create ho gayi hai {location}.",
            "Garbage overflow ne entire street block kar di hai aur epidemic ka threat hai {location}.",
            "Rotten waste se hazardous chemical smell aa rahi hai aur log behosh ho rahe hain {location}."
        ]
    },
    "drainage": {
        "low": [
            "Drain ka paani thoda slow nikal raha hai {location}.",
            "Nali me thodi safai ki zaroorat hai {location}.",
            "Minor drainage issue hai {location}.",
            "Drainage system me halka blockage hai {location}."
        ],
        "medium": [
            "Nali partially block ho gayi hai aur dirty water road par aa raha hai {location}.",
            "Drain overflow kar raha hai aur badboo aa rahi hai {location}.",
            "Nali kafi dino se clean nahi hui hai {location}.",
            "Drainage water jam ho gaya hai {location}."
        ],
        "high": [
            "Drainage system completely block ho gaya hai aur black sewage road pe bhar gaya hai {location}.",
            "Ganda nali ka paani pure area me fail raha hai jisse infection ka khatra hai {location}.",
            "Severe sewage overflow ho raha hai aur movement impossible ho gayi hai {location}.",
            "Drainage fail hone se pura raasta block ho gaya hai {location}."
        ],
        "critical": [
            "Sewage aur drain ka filthy water logon ke houses ke andar ghus gaya hai {location}.",
            "Drain burst ho gaya hai aur contaminated water se bacchon ki jaan ko khatra hai {location}.",
            "Toxic sewage flooding houses, immediate health disaster situation {location}.",
            "Poora drainage system collapse ho gaya hai aur locality trap ho chuki hai {location}."
        ]
    },
    "waterlogging": {
        "low": [
            "Road par thoda sa paani jama hai {location}.",
            "Rain ke baad halka waterlogging hua hai {location}.",
            "Sadak ke kinare thoda paani ruka hai {location}."
        ],
        "medium": [
            "Road par kafi paani bhar gaya hai {location}.",
            "Rain ke baad poori road partially waterlog ho gayi hai {location}.",
            "Waterlogging ki wajah se chalne me dikkat aa rahi hai {location}."
        ],
        "high": [
            "Deep water road par bhar gaya hai aur vehicles doob rahe hain {location}.",
            "Heavy waterlogging ki wajah se traffic totally stall ho chuka hai {location}.",
            "Severe waterlogging se bypass road band ho chuki hai {location}."
        ],
        "critical": [
            "Severe waterlogging se log apne gharon me trap ho gaye hain rescue needed {location}.",
            "Gharon ke andar chest-deep paani ghus gaya hai, drowning ka danger hai {location}.",
            "Emergency situation hai log paani me phas gaye hain bahar nahi nikal sakte {location}."
        ]
    },
    "flood": {
        "low": [
            "River ka water level thoda badh raha hai {location}.",
            "Low-lying area me halka flood water aaya hai {location}.",
            "Minor flooding observe hui hai {location}."
        ],
        "medium": [
            "Locality me flood water fail raha hai {location}.",
            "Sadakon par flood ka paani chad gaya hai {location}.",
            "Flood conditions ban rahi hain {location}."
        ],
        "high": [
            "Severe flooding se pura area doob chuka hai {location}.",
            "Flood water houses aur shops ke andar enter kar chuka hai {location}.",
            "Flood ki wajah se log phans gaye hain aur transport band hai {location}."
        ],
        "critical": [
            "Massive flood me log roofs par stranded hain urgently boat rescue bhejo {location}.",
            "Dangerous flood flow me log behne ki koshish me hain, life-threatening emergency {location}.",
            "Deadly flood situation hai, immediate evacuation and disaster team required {location}."
        ]
    },
    "building_damage": {
        "low": [
            "Building ki outer wall pe choti crack hai {location}.",
            "Building me minor damage dikh raha hai {location}.",
            "Structure ka inspection hona chahiye {location}."
        ],
        "medium": [
            "Building me badi crack develop ho gayi hai {location}.",
            "Building ka ek portion damage ho raha hai {location}.",
            "Structure unsafe lag raha hai {location}."
        ],
        "high": [
            "Building ka major hissa collapse hone ki kagar pe hai, very dangerous {location}.",
            "Building se concrete ke chunks neeche gir rahe hain {location}.",
            "Damaged building heavily tilt ho chuki hai {location}."
        ],
        "critical": [
            "Building fully collapse ho chuki hai aur log debris ke neeche trapped hain {location}.",
            "Apartment building dhas gayi hai immediate rescue and ambulance chahiye {location}.",
            "Structure completely collapsed, multiple lives in critical danger {location}."
        ]
    },
    "landslide": {
        "low": [
            "Hills se thoda mud aur stone road pe gira hai {location}.",
            "Minor landslide hua hai but road abhi open hai {location}."
        ],
        "medium": [
            "Landslide ki wajah se road ka part block ho gaya hai {location}.",
            "Rocks aur debris sadak par aage aa gaye hain {location}."
        ],
        "high": [
            "Huge landslide ne puri road ko completely block kar diya hai {location}.",
            "Massive boulders girne se travel completely unsafe ho gaya hai {location}."
        ],
        "critical": [
            "Massive landslide me multiple vehicles aur log dab gaye hain, urgent SDRF rescue {location}.",
            "Landslide ne houses wipe out kar diye hain, critical life threat {location}."
        ]
    },
    "bridge_damage": {
        "low": [
            "Bridge pe thodi crack notice hui hai {location}.",
            "Bridge ko minor maintenance required hai {location}."
        ],
        "medium": [
            "Bridge ki safety railing toot gayi hai {location}.",
            "Bridge ka ek hissa damage ho chuka hai {location}."
        ],
        "high": [
            "Bridge me heavy structural cracks aa gaye hain, vehicle crossing hazardous hai {location}.",
            "Bridge pillar weaken ho gaya hai kisi bhi time fall ho sakta hai {location}."
        ],
        "critical": [
            "Bridge break ho kar collapse ho gaya hai, connection totally cut off {location}.",
            "Bridge collapse ho chuka hai aur vehicles river me drop ho gaye hain, disaster response {location}."
        ]
    },
    "fire": {
        "low": [
            "Kachre ke chote pile me minor aag lagi hai {location}.",
            "Road side halka smoke nikal raha hai {location}."
        ],
        "medium": [
            "Yahan aag lag gayi hai aur fail rahi hai {location}.",
            "Dry bushes me fire ignite ho chuki hai {location}."
        ],
        "high": [
            "Building me severe fire rapidly spread ho rahi hai {location}.",
            "Flames pass ke houses aur market ki taraf badh rahi hain {location}."
        ],
        "critical": [
            "Aag me log building ke andar trapped hain, fire brigade bhejo jaan ka khatra hai {location}.",
            "Massive fire blast hua hai aur multiple people severely injured hain, emergency response {location}."
        ]
    },
    "water_supply": {
        "low": [
            "Water pressure kafi low aa raha hai {location}.",
            "Aaj water supply thoda late aayi {location}."
        ],
        "medium": [
            "Morning se water supply completely off hai {location}.",
            "Taps me dirty aur muddy water supply ho raha hai {location}."
        ],
        "high": [
            "Pichle 4 days se drinking water bilkul nahi aaya hai, drought jaise haalat {location}.",
            "Main water supply pipeline burst ho gayi hai pura area bina paani ke hai {location}."
        ],
        "critical": [
            "Drinking water pipeline me toxic sewer water mix ho gaya hai, log poison aur hospitalise ho rahe hain {location}.",
            "Contaminated water se epidemic spread ho gaya hai immediate safe tanker supply bhejo {location}."
        ]
    },
    "other": {
        "low": [
            "Yahan ek basic civic problem hai jise check kiya jaye {location}.",
            "Public area ka routine inspection hona chahiye {location}."
        ],
        "medium": [
            "Public infrastructure me problem hone se log trouble face kar rahe hain {location}.",
            "Civic issue ki wajah se locality inconvenience face kar rahi hai {location}."
        ],
        "high": [
            "Severe public issue create ho gaya hai aur residents bahut affected hain {location}.",
            "Major civic problem ki wajah se daily functioning paralyze ho gayi hai {location}."
        ],
        "critical": [
            "Extreme emergency disaster situation hai immediate government help chahiye {location}.",
            "Public hazard create ho gaya hai directly threatening human life {location}."
        ]
    }
}


# ============================================================
# VERIFIED-LANGUAGE PLACEHOLDERS
# ============================================================

VERIFIED_LANGUAGE_TEMPLATES = {
    "sat": [
        "VERIFIED_SANTALI_EXAMPLE_REQUIRED"
    ],

    "nagpuri": [
        "VERIFIED_NAGPURI_SADRI_EXAMPLE_REQUIRED"
    ],

    "mun": [
        "VERIFIED_MUNDARI_EXAMPLE_REQUIRED"
    ],

    "kru": [
        "VERIFIED_KURUKH_ORAON_EXAMPLE_REQUIRED"
    ],

    "ho": [
        "VERIFIED_HO_EXAMPLE_REQUIRED"
    ]
}


# ============================================================
# GENERATE EN / HI / BN / HINGLISH
# ============================================================

def generate_standard_example(language, category, severity):

    if language == "en":
        template = random.choice(
            TEMPLATES[category][severity]
        )

    elif language == "hi":
        template = random.choice(
            HINDI_TEMPLATES[category][severity]
        )

    elif language == "bn":
        template = random.choice(
            BENGALI_TEMPLATES[category][severity]
        )

    elif language == "hinglish":
        template = random.choice(
            HINGLISH_TEMPLATES[category][severity]
        )

    else:
        return None

    location_language = language

    location = random.choice(
        LOCATIONS[location_language]
    )

    return template.format(location=location)


# ============================================================
# GENERATE DATASET
# ============================================================

def generate_dataset():

    rows = []

    standard_languages = [
        "en",
        "hi",
        "bn",
        "hinglish"
    ]

    # We generate only real language examples here.
    # Verified tribal-language examples will be added later.

    while len(rows) < TARGET_ROWS:

        language = random.choice(
            standard_languages
        )

        category = random.choice(
            list(TEMPLATES.keys())
        )

        severity = random.choice([
            "low",
            "medium",
            "high",
            "critical"
        ])

        text = generate_standard_example(
            language,
            category,
            severity
        )

        if not text:
            continue

        # Citizen-style prefixes
        if random.random() < 0.25:

            prefixes = {

                "en": [
                    "Please help, ",
                    "Urgent, ",
                    "I want to report that ",
                    "Please take action, ",
                    "Kindly check, "
                ],

                "hi": [
                    "कृपया मदद करें, ",
                    "जरूरी शिकायत: ",
                    "कृपया ध्यान दें, ",
                    "तुरंत कार्रवाई करें, "
                ],

                "bn": [
                    "দয়া করে সাহায্য করুন, ",
                    "জরুরি অভিযোগ: ",
                    "দয়া করে বিষয়টি দেখুন, ",
                    "তাড়াতাড়ি ব্যবস্থা নিন, "
                ],

                "hinglish": [
                    "Please help, ",
                    "Urgent hai, ",
                    "Please action lo, ",
                    "Kindly check, "
                ]
            }

            text = (
                random.choice(prefixes[language])
                + text
            )

        rows.append({
            "text": text,
            "language": language,
            "category": category,
            "severity": severity
        })

    random.shuffle(rows)

    return rows


# ============================================================
# SAVE DATASET
# ============================================================

def save_dataset(rows):

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "text",
                "language",
                "category",
                "severity"
            ]
        )

        writer.writeheader()
        writer.writerows(rows)


# ============================================================
# STATISTICS
# ============================================================

def show_statistics(rows):

    language_counter = Counter(
        row["language"]
        for row in rows
    )

    category_counter = Counter(
        row["category"]
        for row in rows
    )

    severity_counter = Counter(
        row["severity"]
        for row in rows
    )

    print()
    print("========== DATASET STATISTICS ==========")

    print("\nLanguages:")
    for language, count in language_counter.items():
        print(
            f"  {LANGUAGE_NAMES[language]:20} : {count}"
        )

    print("\nCategories:")
    for category, count in category_counter.items():
        print(
            f"  {category:20} : {count}"
        )

    print("\nSeverity:")
    for severity, count in severity_counter.items():
        print(
            f"  {severity:20} : {count}"
        )

    print("========================================")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("==========================================")
    print(" Samvad Setu - Part A Dataset Generator")
    print("==========================================")

    print()
    print(f"Target rows: {TARGET_ROWS}")

    print()
    print("Generating multilingual civic complaints...")

    rows = generate_dataset()

    save_dataset(rows)

    print()
    print("Dataset generated successfully!")
    print(f"Total rows : {len(rows)}")
    print(f"Output     : {OUTPUT_FILE}")

    show_statistics(rows)

    print()
    print("Supported language architecture:")
    for code, name in LANGUAGE_NAMES.items():
        print(f"  {code:10} -> {name}")

    print()
    print("NOTE:")
    print(
        "Santali, Nagpuri/Sadri, Mundari, Kurukh/Oraon "
        "and Ho require verified native-language examples "
        "before being used for model training."
    )