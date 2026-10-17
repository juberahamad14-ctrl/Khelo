import os
import random
from flask import Flask, render_template_string, request, jsonify, session

app = Flask(__name__)
app.secret_key = "khelo_perfect_bilingual_voice_2026"

IQ_LEVELS = [
    {"iq": "80 IQ", "rank_hi": "नौसिखिया विचारक 🥉", "rank_en": "Novice Thinker 🥉"},
    {"iq": "90 IQ", "rank_hi": "जिज्ञासु मस्तिष्क 🧠", "rank_en": "Curious Mind 🧠"},
    {"iq": "100 IQ", "rank_hi": "तेज दिमाग 🔍", "rank_en": "Sharp Observer 🔍"},
    {"iq": "115 IQ", "rank_hi": "प्रतिभाशाली ज्ञानी ⚡ (सुरक्षित पड़ाव 1)", "rank_en": "Intellect Prodigy ⚡ (Safe Point 1)"},
    {"iq": "125 IQ", "rank_hi": "मास्टरमाइंड 🔮", "rank_en": "Mastermind 🔮"},
    {"iq": "135 IQ", "rank_hi": "उत्कृष्ट विद्वान 🎓", "rank_en": "Elite Scholar 🎓"},
    {"iq": "145 IQ", "rank_hi": "महा ज्ञानी 👑 (सुरक्षित पड़ाव 2)", "rank_en": "Grand Polymath 👑 (Safe Point 2)"},
    {"iq": "155 IQ", "rank_hi": "दूरदर्शी मस्तिष्क 🌌", "rank_en": "Supreme Visionary 🌌"},
    {"iq": "165 IQ", "rank_hi": "ब्रह्मांडीय प्रतिभा 🧬", "rank_en": "Cosmic Genius 🧬"},
    {"iq": "180+ IQ", "rank_hi": "सर्वोच्च लीजेंड 🌟", "rank_en": "Neural Transcendence 🌟"}
]

# 10 Sets: Pure Hindi aur Pure English alag-alag
KHELO_SETS = {
    1: {
        "title_hi": "सेट 1: भारत का इतिहास और राष्ट्रीय प्रतीक",
        "title_en": "Set 1: Indian History and National Symbols",
        "questions": [
            {
                "hi": {"q": "भारत का राष्ट्रीय पशु कौन सा है?", "options": ["शेर", "बाघ (रॉयल बंगाल टाइगर)", "हाथी", "चीता"]},
                "en": {"q": "Which is the National Animal of India?", "options": ["Lion", "Bengal Tiger", "Elephant", "Cheetah"]},
                "ans": 1
            },
            {
                "hi": {"q": "भारत के राष्ट्रपति भवन का डिजाइन किसने बनाया था?", "options": ["एडविन लुटियंस", "ली कोर्बुसिए", "हर्बर्ट बेकर", "चार्ल्स कोरिया"]},
                "en": {"q": "Who designed the Rashtrapati Bhavan of India?", "options": ["Edwin Lutyens", "Le Corbusier", "Herbert Baker", "Charles Correa"]},
                "ans": 0
            },
            {
                "hi": {"q": "1857 के स्वतंत्रता संग्राम के पहले शहीद कौन थे?", "options": ["भगत सिंह", "तात्या टोपे", "मंगल पांडे", "नाना साहेब"]},
                "en": {"q": "Who was the first martyr of the 1857 Indian revolt?", "options": ["Bhagat Singh", "Tantia Tope", "Mangal Pandey", "Nana Saheb"]},
                "ans": 2
            },
            {
                "hi": {"q": "जलियांवाला बाग हत्याकांड किस वर्ष हुआ था?", "options": ["1919", "1920", "1915", "1922"]},
                "en": {"q": "In which year did the Jallianwala Bagh massacre take place?", "options": ["1919", "1920", "1915", "1922"]},
                "ans": 0
            },
            {
                "hi": {"q": "आर्य समाज की स्थापना किसने की थी?", "options": ["राजा राममोहन राय", "स्वामी दयानंद सरस्वती", "स्वामी विवेकानंद", "ईश्वर चंद्र विद्यासागर"]},
                "en": {"q": "Who founded the Arya Samaj?", "options": ["Raja Ram Mohan Roy", "Swami Dayanand Saraswati", "Swami Vivekananda", "Ishwar Chandra Vidyasagar"]},
                "ans": 1
            },
            {
                "hi": {"q": "भारत के पहले उपराष्ट्रपति कौन थे?", "options": ["डॉ सर्वपल्ली राधाकृष्णन", "डॉ जाकिर हुसैन", "वी वी गिरि", "डॉ राजेंद्र प्रसाद"]},
                "en": {"q": "Who was the first Vice President of India?", "options": ["Dr. S. Radhakrishnan", "Dr. Zakir Husain", "V. V. Giri", "Dr. Rajendra Prasad"]},
                "ans": 0
            },
            {
                "hi": {"q": "महात्मा गांधी ने दांडी मार्च किस वर्ष शुरू किया था?", "options": ["1928", "1930", "1932", "1942"]},
                "en": {"q": "In which year did Mahatma Gandhi initiate the Dandi March?", "options": ["1928", "1930", "1932", "1942"]},
                "ans": 1
            },
            {
                "hi": {"q": "हड़प्पा सभ्यता की खोज किस वर्ष हुई थी?", "options": ["1921", "1911", "1935", "1942"]},
                "en": {"q": "In which year was the ancient Harappan civilization discovered?", "options": ["1921", "1911", "1935", "1942"]},
                "ans": 0
            },
            {
                "hi": {"q": "स्वतंत्र भारत के अंतिम गवर्नर जनरल कौन थे?", "options": ["लॉर्ड माउंटबेटन", "सी राजगोपालाचारी", "लॉर्ड कैनिंग", "जवाहरलाल नेहरू"]},
                "en": {"q": "Who was the last Governor-General of independent India?", "options": ["Lord Mountbatten", "C. Rajagopalachari", "Lord Canning", "Jawaharlal Nehru"]},
                "ans": 1
            },
            {
                "hi": {"q": "सम्राट अशोक के शिलालेखों को सबसे पहले किसने पढ़ा था?", "options": ["जेम्स प्रिंसेप", "अलेक्जेंडर कनिंघम", "मैक्स मूलर", "मॉर्टिमर व्हीलर"]},
                "en": {"q": "Who was the first scholar to decipher Emperor Ashoka's edicts?", "options": ["James Prinsep", "Alexander Cunningham", "Max Muller", "Mortimer Wheeler"]},
                "ans": 0
            }
        ]
    },
    2: {
        "title_hi": "सेट 2: विज्ञान और ब्रह्मांड",
        "title_en": "Set 2: Science and Universe",
        "questions": [
            {
                "hi": {"q": "हमारे सौरमंडल का सबसे बड़ा ग्रह कौन सा है?", "options": ["मंगल ग्रह", "बृहस्पति ग्रह", "शनि ग्रह", "पृथ्वी"]},
                "en": {"q": "Which is the largest planet in our solar system?", "options": ["Mars", "Jupiter", "Saturn", "Earth"]},
                "ans": 1
            },
            {
                "hi": {"q": "वयस्क मानव शरीर में कुल कितनी हड्डियां होती हैं?", "options": ["198", "206", "212", "208"]},
                "en": {"q": "How many bones are present in an adult human body?", "options": ["198", "206", "212", "208"]},
                "ans": 1
            },
            {
                "hi": {"q": "प्रकाश की चाल लगभग कितनी होती है?", "options": ["3 लाख किलोमीटर प्रति सेकंड", "1.5 लाख किलोमीटर प्रति सेकंड", "5 लाख किलोमीटर प्रति सेकंड", "30 हजार किलोमीटर प्रति सेकंड"]},
                "en": {"q": "What is the approximate speed of light in vacuum?", "options": ["300,000 km per second", "150,000 km per second", "500,000 km per second", "30,000 km per second"]},
                "ans": 0
            },
            {
                "hi": {"q": "शुद्ध जल का रासायनिक सूत्र क्या है?", "options": ["CO2", "H2O", "O2", "NaCl"]},
                "en": {"q": "What is the chemical formula of pure water?", "options": ["CO2", "H2O", "O2", "NaCl"]},
                "ans": 1
            },
            {
                "hi": {"q": "सौरमंडल के किस ग्रह को लाल ग्रह कहा जाता है?", "options": ["शुक्र ग्रह", "मंगल ग्रह", "बुध ग्रह", "बृहस्पति ग्रह"]},
                "en": {"q": "Which planet is known as the Red Planet?", "options": ["Venus", "Mars", "Mercury", "Jupiter"]},
                "ans": 1
            },
            {
                "hi": {"q": "डीएनए की डबल हेलिक्स संरचना की खोज किसने की थी?", "options": ["वाटसन और क्रिक", "आइजैक न्यूटन", "अल्बर्ट आइंस्टीन", "लुई पाश्चर"]},
                "en": {"q": "Who discovered the double-helix structure of DNA?", "options": ["Watson and Crick", "Isaac Newton", "Albert Einstein", "Louis Pasteur"]},
                "ans": 0
            },
            {
                "hi": {"q": "सूर्य की धूप से हमारे शरीर को कौन सा विटामिन मिलता है?", "options": ["विटामिन ए", "विटामिन सी", "विटामिन डी", "विटामिन बी12"]},
                "en": {"q": "Which vitamin is synthesized in our body via sunlight?", "options": ["Vitamin A", "Vitamin C", "Vitamin D", "Vitamin B12"]},
                "ans": 2
            },
            {
                "hi": {"q": "ध्वनि की तरंगें किस माध्यम में यात्रा नहीं कर सकतीं?", "options": ["पानी में", "हवा में", "निर्वात (वैक्यूम) में", "लोहे में"]},
                "en": {"q": "Through which medium can sound waves not travel?", "options": ["Water", "Air", "Vacuum", "Iron"]},
                "ans": 2
            },
            {
                "hi": {"q": "पेड़-पौधों में मौजूद क्लोरोफिल का मुख्य रंग क्या होता है?", "options": ["पीला", "हरा", "नीला", "लाल"]},
                "en": {"q": "What is the primary color of chlorophyll in green plants?", "options": ["Yellow", "Green", "Blue", "Red"]},
                "ans": 1
            },
            {
                "hi": {"q": "वैज्ञानिक हिग्स बोसोन कण को सामान्यतः क्या कहते हैं?", "options": ["गॉड पार्टिकल", "सुपर क्वार्क", "डार्क एटम", "कॉस्मिक कण"]},
                "en": {"q": "What is the Higgs Boson particle popularly nicknamed?", "options": ["God Particle", "Super Quark", "Dark Atom", "Cosmic Ray"]},
                "ans": 0
            }
        ]
    },
    3: {
        "title_hi": "सेट 3: खेल जगत और क्रिकेट",
        "title_en": "Set 3: Sports and Athletics",
        "questions": [
            {
                "hi": {"q": "1983 के क्रिकेट विश्व कप में भारत के कप्तान कौन थे?", "options": ["सुनील गावस्कर", "कपिल देव", "मोहिंदर अमरनाथ", "रवि शास्त्री"]},
                "en": {"q": "Who was India's captain during the 1983 Cricket World Cup?", "options": ["Sunil Gavaskar", "Kapil Dev", "Mohinder Amarnath", "Ravi Shastri"]},
                "ans": 1
            },
            {
                "hi": {"q": "ओलंपिक के प्रतीक चिन्ह में कुल कितने छल्ले होते हैं?", "options": ["चार", "पांच", "छह", "सात"]},
                "en": {"q": "How many colored rings are in the official Olympic symbol?", "options": ["Four", "Five", "Six", "Seven"]},
                "ans": 1
            },
            {
                "hi": {"q": "बैडमिंटन की शटलकॉक में कुल कितने पंख लगाए जाते हैं?", "options": ["14 पंख", "16 पंख", "18 पंख", "12 पंख"]},
                "en": {"q": "How many feathers are traditionally embedded in a badminton shuttlecock?", "options": ["14 Feathers", "16 Feathers", "18 Feathers", "12 Feathers"]},
                "ans": 1
            },
            {
                "hi": {"q": "मास्टर ब्लास्टर के नाम से किस महान क्रिकेटर को जाना जाता है?", "options": ["विराट कोहली", "सचिन तेंदुलकर", "महेंद्र सिंह धोनी", "रोहित शर्मा"]},
                "en": {"q": "Which cricket icon is universally known as Master Blaster?", "options": ["Virat Kohli", "Sachin Tendulkar", "MS Dhoni", "Rohit Sharma"]},
                "ans": 1
            },
            {
                "hi": {"q": "फुटबॉल मैच की सामान्य समयावधि कितनी होती है?", "options": ["80 मिनट", "90 मिनट", "100 मिनट", "60 मिनट"]},
                "en": {"q": "What is the official regulation playing time of a football match?", "options": ["80 Minutes", "90 Minutes", "100 Minutes", "60 Minutes"]},
                "ans": 1
            },
            {
                "hi": {"q": "भारत का सबसे पुराना फुटबॉल टूर्नामेंट कौन सा है?", "options": ["संतोष ट्रॉफी", "डूरंड कप", "आई-लीग", "आईएसएल"]},
                "en": {"q": "Which is the oldest football tournament in India?", "options": ["Santosh Trophy", "Durand Cup", "I-League", "ISL"]},
                "ans": 1
            },
            {
                "hi": {"q": "प्रसिद्ध विंबलडन चैंपियनशिप किस खेल से जुड़ी हुई है?", "options": ["टेनिस", "गोल्फ", "पोलो", "स्क्वैश"]},
                "en": {"q": "The prestigious Wimbledon Championship is associated with which sport?", "options": ["Tennis", "Golf", "Polo", "Squash"]},
                "ans": 0
            },
            {
                "hi": {"q": "शतरंज के बोर्ड पर कुल कितने चौकोर वर्ग होते हैं?", "options": ["56", "64", "72", "81"]},
                "en": {"q": "How many squares are there on a standard chess board?", "options": ["56", "64", "72", "81"]},
                "ans": 1
            },
            {
                "hi": {"q": "ओलंपिक स्वर्ण पदक विजेता नीरज चोपड़ा किस खेल से संबंधित हैं?", "options": ["शॉटपुट", "भाला फेंक (जैवलिन थ्रो)", "लंबी कूद", "मुक्केबाजी"]},
                "en": {"q": "Olympic gold medalist Neeraj Chopra is associated with which sport?", "options": ["Shotput", "Javelin Throw", "Long Jump", "Boxing"]},
                "ans": 1
            },
            {
                "hi": {"q": "पहले आधुनिक ओलंपिक खेल 1896 में किस शहर में आयोजित हुए थे?", "options": ["पेरिस", "लंदन", "एथेंस", "रोम"]},
                "en": {"q": "In which city were the first modern Olympic Games held in 1896?", "options": ["Paris", "London", "Athens", "Rome"]},
                "ans": 2
            }
        ]
    },
    4: {
        "title_hi": "सेट 4: भूगोल और नदियां",
        "title_en": "Set 4: Geography and Rivers",
        "questions": [
            {
                "hi": {"q": "विश्व की सबसे लंबी नदी कौन सी है?", "options": ["अमेजन नदी", "नील नदी", "गंगा नदी", "यांग्त्से नदी"]},
                "en": {"q": "Which is the longest river in the world?", "options": ["Amazon River", "Nile River", "Ganga River", "Yangtze River"]},
                "ans": 1
            },
            {
                "hi": {"q": "भारत की सबसे लंबी नदी कौन सी मानी जाती है?", "options": ["यमुना नदी", "गोदावरी नदी", "गंगा नदी", "ब्रह्मपुत्र नदी"]},
                "en": {"q": "Which is the longest river flowing through India?", "options": ["Yamuna River", "Godavari River", "Ganga River", "Brahmaputra River"]},
                "ans": 2
            },
            {
                "hi": {"q": "दुनिया की सबसे ऊंची चोटी माउंट एवरेस्ट किस देश में स्थित है?", "options": ["भारत", "नेपाल", "चीन", "भूटान"]},
                "en": {"q": "Mount Everest is situated in which country?", "options": ["India", "Nepal", "China", "Bhutan"]},
                "ans": 1
            },
            {
                "hi": {"q": "पृथ्वी का सबसे बड़ा और गहरा महासागर कौन सा है?", "options": ["अटलांटिक महासागर", "प्रशांत महासागर", "हिंद महासागर", "आर्कटिक महासागर"]},
                "en": {"q": "Which is the largest and deepest ocean on Earth?", "options": ["Atlantic Ocean", "Pacific Ocean", "Indian Ocean", "Arctic Ocean"]},
                "ans": 1
            },
            {
                "hi": {"q": "कोलकाता शहर किस नदी के तट पर बसा हुआ है?", "options": ["गंगा नदी", "हुगली नदी", "यमुना नदी", "महानदी"]},
                "en": {"q": "The city of Kolkata is situated along the banks of which river?", "options": ["Ganga River", "Hooghly River", "Yamuna River", "Mahanadi River"]},
                "ans": 1
            },
            {
                "hi": {"q": "दुनिया का सबसे बड़ा गर्म रेगिस्तान कौन सा है?", "options": ["थार मरुस्थल", "गोबी मरुस्थल", "सहारा मरुस्थल", "कालाहारी मरुस्थल"]},
                "en": {"q": "Which is the largest subtropical hot desert in the world?", "options": ["Thar Desert", "Gobi Desert", "Sahara Desert", "Kalahari Desert"]},
                "ans": 2
            },
            {
                "hi": {"q": "भारत के किस राज्य को 'चाय का बागान' कहा जाता है?", "options": ["केरल", "असम", "पश्चिम बंगाल", "कर्नाटक"]},
                "en": {"q": "Which Indian state is famously known as the Tea Garden of India?", "options": ["Kerala", "Assam", "West Bengal", "Karnataka"]},
                "ans": 1
            },
            {
                "hi": {"q": "क्षेत्रफल के हिसाब से भारत का सबसे छोटा राज्य कौन सा है?", "options": ["सिक्किम", "गोवा", "त्रिपुरा", "मणिपुर"]},
                "en": {"q": "Which is the smallest Indian state by land area?", "options": ["Sikkim", "Goa", "Tripura", "Manipur"]},
                "ans": 1
            },
            {
                "hi": {"q": "स्वेज नहर किन दो प्रमुख समुद्रों को आपस में जोड़ती है?", "options": ["लाल सागर और भूमध्य सागर", "काला सागर और लाल सागर", "अटलांटिक और प्रशांत महासागर", "अरब सागर और बंगाल की खाड़ी"]},
                "en": {"q": "The Suez Canal connects which two bodies of water?", "options": ["Red Sea and Mediterranean Sea", "Black Sea and Red Sea", "Atlantic and Pacific", "Arabian Sea and Bay of Bengal"]},
                "ans": 0
            },
            {
                "hi": {"q": "विश्व की सबसे गहरी मीठे पानी की झील कौन सी है?", "options": ["सुपीरियर झील", "बैकाल झील", "कैस्पियन सागर", "विक्टोरिया झील"]},
                "en": {"q": "Which is the deepest freshwater lake on Earth?", "options": ["Lake Superior", "Lake Baikal", "Caspian Sea", "Lake Victoria"]},
                "ans": 1
            }
        ]
    },
    5: {
        "title_hi": "सेट 5: कंप्यूटर और इंटरनेट",
        "title_en": "Set 5: Computer and Internet",
        "questions": [
            {
                "hi": {"q": "कंप्यूटर का मस्तिष्क किसे कहा जाता है?", "options": ["रैम (RAM)", "मॉनिटर", "सीपीयू (CPU)", "हार्ड डिस्क"]},
                "en": {"q": "Which component is known as the brain of a computer?", "options": ["RAM", "Monitor", "CPU", "Hard Disk"]},
                "ans": 2
            },
            {
                "hi": {"q": "इंटरनेट में WWW का पूरा अर्थ क्या होता है?", "options": ["वर्ल्ड वाइड वेब", "वर्ल्ड वाइल्ड वेब", "वाइड वर्ल्ड वेब", "वेब वर्ल्ड वाइड"]},
                "en": {"q": "What is the full form of WWW in internet terminology?", "options": ["World Wide Web", "World Wild Web", "Wide World Web", "Web World Wide"]},
                "ans": 0
            },
            {
                "hi": {"q": "पायथन प्रोग्रामिंग भाषा का निर्माण किसने किया था?", "options": ["डेनिस रिची", "गिडो वैन रॉसम", "जेम्स गोस्लिंग", "बजार्ने स्ट्रॉस्ट्रुप"]},
                "en": {"q": "Who created the Python programming language?", "options": ["Dennis Ritchie", "Guido van Rossum", "James Gosling", "Bjarne Stroustrup"]},
                "ans": 1
            },
            {
                "hi": {"q": "कीबोर्ड की सबसे ऊपरी F1 से F12 कीज को क्या कहते हैं?", "options": ["अल्फा कीज", "फंक्शन कीज", "न्यूमेरिक कीज", "कंट्रोल कीज"]},
                "en": {"q": "What are keys F1 through F12 called on a computer keyboard?", "options": ["Alpha Keys", "Function Keys", "Numeric Keys", "Control Keys"]},
                "ans": 1
            },
            {
                "hi": {"q": "गूगल सर्च इंजन की स्थापना किस वर्ष हुई थी?", "options": ["1995", "1998", "2001", "2004"]},
                "en": {"q": "In which year was Google formally founded?", "options": ["1995", "1998", "2001", "2004"]},
                "ans": 1
            },
            {
                "hi": {"q": "एक मेगाबाइट (MB) में कुल कितने किलोबाइट (KB) होते हैं?", "options": ["1000 KB", "1024 KB", "512 KB", "2048 KB"]},
                "en": {"q": "How many Kilobytes are in one Megabyte?", "options": ["1000 KB", "1024 KB", "512 KB", "2048 KB"]},
                "ans": 1
            },
            {
                "hi": {"q": "HTML का उपयोग मुख्य रूप से क्या बनाने के लिए किया जाता है?", "options": ["ऑपरेटिंग सिस्टम", "वेब पेज", "वीडियो गेम", "माइक्रोचिप"]},
                "en": {"q": "HTML is primarily used to build which digital product?", "options": ["Operating Systems", "Web Pages", "Video Games", "Microchips"]},
                "ans": 1
            },
            {
                "hi": {"q": "आर्टिफिशियल इंटेलिजेंस शब्द सबसे पहले किसने दिया था?", "options": ["जॉन मैकार्थी", "एलन ट्यूरिंग", "एलोन मस्क", "बिल गेट्स"]},
                "en": {"q": "Who originally coined the term Artificial Intelligence in 1956?", "options": ["John McCarthy", "Alan Turing", "Elon Musk", "Bill Gates"]},
                "ans": 0
            },
            {
                "hi": {"q": "लिनक्स (Linux) किस प्रकार का सॉफ्टवेयर है?", "options": ["वेब ब्राउज़र", "ओपन सोर्स ऑपरेटिंग सिस्टम", "एंटीवायरस", "हार्डवेयर कार्ड"]},
                "en": {"q": "What type of software is Linux?", "options": ["Web Browser", "Open Source Operating System", "Antivirus", "Hardware Card"]},
                "ans": 1
            },
            {
                "hi": {"q": "बिटकॉइन क्रिप्टो करेंसी के अज्ञात निर्माता का नाम क्या है?", "options": ["विटालिक बुटेरिन", "सातोशी नाकामोतो", "लिनस टोरवाल्ड्स", "मार्क जुकरबर्ग"]},
                "en": {"q": "What is the pseudonymous name of Bitcoin's creator?", "options": ["Vitalik Buterin", "Satoshi Nakamoto", "Linus Torvalds", "Mark Zuckerberg"]},
                "ans": 1
            }
        ]
    },
    6: {
        "title_hi": "सेट 6: सिनेमा और मनोरंजन",
        "title_en": "Set 6: Cinema and Entertainment",
        "questions": [
            {
            "hi": {"q": "भारत की पहली सवाक यानी बोलती फिल्म कौन सी थी?", "options": ["राजा हरिश्चंद्र", "आलम आरा", "किसान कन्या", "मुगल-ए-आज़म"]},
                "en": {"q": "Which was India's first sound motion picture?", "options": ["Raja Harishchandra", "Alam Ara", "Kisan Kanya", "Mughal-E-Azam"]},
                "ans": 1
            },
            {
                "hi": {"q": "फिल्म शोले में डाकू गब्बर सिंह का किरदार किसने निभाया था?", "options": ["प्राण", "अमजद खान", "अमरीश पुरी", "डैनी डेन्जोंगपा"]},
                "en": {"q": "Who portrayed the iconic dacoit Gabbar Singh in Sholay?", "options": ["Pran", "Amjad Khan", "Amrish Puri", "Danny Denzongpa"]},
                "ans": 1
            },
            {
                "hi": {"q": "प्रसिद्ध फिल्म लगान के निर्देशक कौन थे?", "options": ["आशुतोष गोवारिकर", "संजय लीला भंसाली", "करण जौहर", "राकेश ओमप्रकाश मेहरा"]},
                "en": {"q": "Who directed the Oscar-nominated film Lagaan?", "options": ["Ashutosh Gowariker", "Sanjay Leela Bhansali", "Karan Johar", "Rakeysh Mehra"]},
                "ans": 0
            },
            {
                "hi": {"q": "ऑस्कर पुरस्कार जीतने वाले पहले भारतीय व्यक्ति कौन थे?", "options": ["सत्यजीत रे", "भानु अथैया", "ए आर रहमान", "गुलजार"]},
                "en": {"q": "Who was the first Indian citizen to win an Oscar?", "options": ["Satyajit Ray", "Bhanu Athaiya", "A. R. Rahman", "Gulzar"]},
                "ans": 1
            },
            {
                "hi": {"q": "दादा साहेब फाल्के पुरस्कार किस क्षेत्र का सर्वोच्च सम्मान है?", "options": ["खेल जगत", "भारतीय सिनेमा", "साहित्य", "विज्ञान"]},
                "en": {"q": "The Dadasaheb Phalke award is presented in which discipline?", "options": ["Sports", "Cinema", "Literature", "Science"]},
                "ans": 1
            },
            {
                "hi": {"q": "फिल्म '3 इडियट्स' चेतन भगत के किस उपन्यास पर आधारित थी?", "options": ["हाफ गर्लफ्रेंड", "फाइव पॉइंट समवन", "टू स्टेट्स", "थ्री मिस्टेक्स ऑफ माय लाइफ"]},
                "en": {"q": "The Bollywood movie 3 Idiots was based on which novel?", "options": ["Half Girlfriend", "Five Point Someone", "2 States", "3 Mistakes of My Life"]},
                "ans": 1
            },
            {
                "hi": {"q": "सत्यजीत रे को लाइफटाइम अचीवमेंट ऑस्कर किस वर्ष दिया गया था?", "options": ["1992", "1988", "1995", "1985"]},
                "en": {"q": "In which year was director Satyajit Ray awarded an Honorary Oscar?", "options": ["1992", "1988", "1995", "1985"]},
                "ans": 0
            },
            {
                "hi": {"q": "ऑस्कर विजेता गीत 'नाटू नाटू' के संगीतकार कौन हैं?", "options": ["एम एम कीरावनी", "ए आर रहमान", "प्रीतम", "अनिरुद्ध रविचंदर"]},
                "en": {"q": "Who composed the Oscar-winning original song 'Naatu Naatu'?", "options": ["M. M. Keeravani", "A. R. Rahman", "Pritam", "Anirudh Ravichander"]},
                "ans": 0
            },
            {
                "hi": {"q": "फिल्म मुगल-ए-आज़म में शहंशाह अकबर की भूमिका किसने निभाई थी?", "options": ["दिलीप कुमार", "पृथ्वीराज कपूर", "संजीव कुमार", "बलराज साहनी"]},
                "en": {"q": "Who played Emperor Akbar in the classic movie Mughal-E-Azam?", "options": ["Dilip Kumar", "Prithviraj Kapoor", "Sanjeev Kumar", "Balraj Sahni"]},
                "ans": 1
            },
            {
                "hi": {"q": "भारत की पहली 3डी फिल्म कौन सी मानी जाती है?", "options": ["शिवा का इंसाफ", "माय डियर कुट्टीचाथन", "छोटा चेतन", "रा वन"]},
                "en": {"q": "Which is recognized as India's first 3D feature movie?", "options": ["Shiva Ka Insaaf", "My Dear Kuttichathan", "Chhota Chetan", "Ra.One"]},
                "ans": 1
            }
        ]
    },
    7: {
        "title_hi": "सेट 7: राजनीति और भारतीय संविधान",
        "title_en": "Set 7: Polity and Constitution",
        "questions": [
            {
                "hi": {"q": "भारतीय संविधान का जनक या पितामह किसे कहा जाता है?", "options": ["महात्मा गांधी", "डॉ भीमराव अंबेडकर", "जवाहरलाल नेहरू", "सरदार वल्लभभाई पटेल"]},
                "en": {"q": "Who is known as the Father of the Indian Constitution?", "options": ["Mahatma Gandhi", "Dr. B. R. Ambedkar", "Jawaharlal Nehru", "Sardar Patel"]},
                "ans": 1
            },
            {
                "hi": {"q": "भारत में नागरिक मताधिकार की न्यूनतम आयु क्या तय है?", "options": ["21 वर्ष", "18 वर्ष", "20 वर्ष", "16 वर्ष"]},
                "en": {"q": "What is the official minimum voting age in India?", "options": ["21 Years", "18 Years", "20 Years", "16 Years"]},
                "ans": 1
            },
            {
                "hi": {"q": "लोकसभा के निर्वाचित सदस्यों का कार्यकाल कितने वर्ष का होता है?", "options": ["6 वर्ष", "5 वर्ष", "4 वर्ष", "स्थायी"]},
                "en": {"q": "What is the standard tenure of Lok Sabha members?", "options": ["6 Years", "5 Years", "4 Years", "Permanent"]},
                "ans": 1
            },
            {
                "hi": {"q": "भारतीय संविधान निर्माण में कुल कितना समय लगा था?", "options": ["2 वर्ष 11 महीने 18 दिन", "3 वर्ष 5 महीने", "1 वर्ष 8 महीने", "4 वर्ष"]},
                "en": {"q": "How long did it take to complete the Indian Constitution?", "options": ["2 years 11 months 18 days", "3 years 5 months", "1 year 8 months", "4 years"]},
                "ans": 0
            },
            {
                "hi": {"q": "भारत के मुख्य न्यायाधीश की नियुक्ति कौन करता है?", "options": ["प्रधानमंत्री", "राष्ट्रपति", "संसद", "विधि मंत्री"]},
                "en": {"q": "Who appoints the Chief Justice of India?", "options": ["Prime Minister", "President", "Parliament", "Law Minister"]},
                "ans": 1
            },
            {
                "hi": {"q": "संविधान में मौलिक अधिकार किस देश के संविधान से प्रेरित हैं?", "options": ["ब्रिटेन", "संयुक्त राज्य अमेरिका (USA)", "रूस", "कनाडा"]},
                "en": {"q": "Fundamental Rights were adopted from which nation's constitution?", "options": ["United Kingdom", "USA", "Russia", "Canada"]},
                "ans": 1
            },
            {
                "hi": {"q": "राज्यसभा के पदेन सभापति का पद कौन संभालता है?", "options": ["राष्ट्रपति", "उपराष्ट्रपति", "लोकसभा अध्यक्ष", "प्रधानमंत्री"]},
                "en": {"q": "Who serves as the ex-officio Chairman of the Rajya Sabha?", "options": ["President", "Vice President", "Speaker", "Prime Minister"]},
                "ans": 1
            },
            {
                "hi": {"q": "विशेष अनुच्छेद 370 किस राज्य से संबंधित था?", "options": ["असम", "जम्मू और कश्मीर", "पंजाब", "नागालैंड"]},
                "en": {"q": "Article 370 was associated with which former state?", "options": ["Assam", "Jammu and Kashmir", "Punjab", "Nagaland"]},
                "ans": 1
            },
            {
                "hi": {"q": "भारत में पंचायती राज व्यवस्था सबसे पहले किस राज्य में लागू हुई?", "options": ["राजस्थान", "आंध्र प्रदेश", "गुजरात", "उत्तर प्रदेश"]},
                "en": {"q": "Panchayati Raj was first introduced in which Indian state?", "options": ["Rajasthan", "Andhra Pradesh", "Gujarat", "Uttar Pradesh"]},
                "ans": 0
            },
            {
                "hi": {"q": "संविधान के किस संशोधन को 'लघु संविधान' कहा जाता है?", "options": ["42वां संविधान संशोधन", "44वां संशोधन", "73वां संशोधन", "86वां संशोधन"]},
                "en": {"q": "Which constitutional amendment is known as the Mini Constitution?", "options": ["42nd Amendment", "44th Amendment", "73rd Amendment", "86th Amendment"]},
                "ans": 0
            }
        ]
    },
    8: {
        "title_hi": "सेट 8: साहित्य और कला",
        "title_en": "Set 8: Literature and Art",
        "questions": [
            {
                "hi": {"q": "महाकाव्य रामचरितमानस की रचना किसने की थी?", "options": ["महर्षि वाल्मीकि", "गोस्वामी तुलसीदास", "सूरदास", "संत कबीर"]},
                "en": {"q": "Who composed the sacred epic poem Ramcharitmanas?", "options": ["Valmiki", "Goswami Tulsidas", "Surdas", "Kabir"]},
                "ans": 1
            },
            {
                "hi": {"q": "साहित्य में नोबेल पुरस्कार पाने वाले प्रथम भारतीय कौन थे?", "options": ["सी वी रमन", "रवींद्रनाथ टैगोर", "मदर टेरेसा", "अमर्त्य सेन"]},
                "en": {"q": "Who was the first Indian to receive a Nobel Prize?", "options": ["C. V. Raman", "Rabindranath Tagore", "Mother Teresa", "Amartya Sen"]},
                "ans": 1
            },
            {
                "hi": {"q": "मोनालिसा की प्रसिद्ध पेंटिंग के चित्रकार कौन थे?", "options": ["पाब्लो पिकासो", "लियोनार्डो दा विंची", "विंसेंट वैन गॉग", "माइकल एंजेलो"]},
                "en": {"q": "Who painted the masterwork portrait Mona Lisa?", "options": ["Pablo Picasso", "Leonardo da Vinci", "Vincent van Gogh", "Michelangelo"]},
                "ans": 1
            },
            {
                "hi": {"q": "प्रसिद्ध कालजयी उपन्यास 'गोदान' के लेखक कौन हैं?", "options": ["मुंशी प्रेमचंद", "हरिवंश राय बच्चन", "जयशंकर प्रसाद", "रामधारी सिंह दिनकर"]},
                "en": {"q": "Who authored the classic realistic novel 'Godan'?", "options": ["Munshi Premchand", "Harivansh Rai Bachchan", "Jaishankar Prasad", "Ramdhari Dinkar"]},
                "ans": 0
            },
            {
                "hi": {"q": "कविता संग्रह 'मधुशाला' किसकी अमर कृति है?", "options": ["हरिवंश राय बच्चन", "मैथिलीशरण गुप्त", "महादेवी वर्मा", "दुष्यंत कुमार"]},
                "en": {"q": "Who wrote the famous poetic anthology 'Madhushala'?", "options": ["Harivansh Rai Bachchan", "Maithili Sharan Gupt", "Mahadevi Verma", "Dushyant Kumar"]},
                "ans": 0
            },
            {
                "hi": {"q": "महाभारत महाकाव्य की रचना किस महर्षि ने की थी?", "options": ["महर्षि वाल्मीकि", "महर्षि वेदव्यास", "महर्षि वशिष्ठ", "महर्षि विश्वामित्र"]},
                "en": {"q": "Which sage authored the timeless epic Mahabharata?", "options": ["Valmiki", "Ved Vyas", "Vashistha", "Vishwamitra"]},
                "ans": 1
            },
            {
                "hi": {"q": "भरत मुनि का 'नाट्यशास्त्र' किस विषय का प्राचीनतम ग्रंथ है?", "options": ["चिकित्सा शास्त्र", "नाटक और शास्त्रीय नृत्य", "खगोल विज्ञान", "कृषि"]},
                "en": {"q": "Bharata Muni's 'Natya Shastra' is an ancient treatise on what?", "options": ["Medicine", "Performing Arts and Dance", "Astronomy", "Agriculture"]},
                "ans": 1
            },
            {
                "hi": {"q": "मधुबनी चित्रकला किस राज्य की पारंपरिक लोककला है?", "options": ["बिहार", "राजस्थान", "मध्य प्रदेश", "ओडिशा"]},
                "en": {"q": "Madhubani folk painting originated in which Indian state?", "options": ["Bihar", "Rajasthan", "Madhya Pradesh", "Odisha"]},
                "ans": 0
            },
            {
                "hi": {"q": "हैरी पॉटर पुस्तक श्रृंखला की प्रसिद्ध लेखिका कौन हैं?", "options": ["अगाथा क्रिस्टी", "जे के रोलिंग", "एनिड ब्लाइटन", "वर्जीनिया वुल्फ"]},
                "en": {"q": "Who authored the globally acclaimed Harry Potter series?", "options": ["Agatha Christie", "J. K. Rowling", "Enid Blyton", "Virginia Woolf"]},
                "ans": 1
            },
            {
                "hi": {"q": "पंचतंत्र की प्रसिद्ध नीति कथाओं के रचनाकार कौन हैं?", "options": ["पंडित विष्णु शर्मा", "कालिदास", "आचार्य चाणक्य", "भवभूति"]},
                "en": {"q": "Who is credited with creating the fables of Panchatantra?", "options": ["Vishnu Sharma", "Kalidasa", "Chanakya", "Bhavabhuti"]},
                "ans": 0
            }
        ]
    },
    9: {
        "title_hi": "सेट 9: पर्यावरण और प्रकृति",
        "title_en": "Set 9: Nature and Environment",
        "questions": [
            {
                "hi": {"q": "विश्व पर्यावरण दिवस प्रतिवर्ष किस तारीख को मनाया जाता है?", "options": ["5 जून", "22 अप्रैल", "16 सितंबर", "1 दिसंबर"]},
                "en": {"q": "When is World Environment Day commemorated globally?", "options": ["June 5", "April 22", "September 16", "December 1"]},
                "ans": 0
            },
            {
                "hi": {"q": "ओजोन परत हमें सूर्य की किन हानिकारक किरणों से बचाती है?", "options": ["इन्फ्रारेड किरणें", "पराबैंगनी (UV) किरणें", "गामा किरणें", "एक्स किरणें"]},
                "en": {"q": "The ozone layer shields Earth from which solar rays?", "options": ["Infrared Rays", "Ultraviolet (UV) Rays", "Gamma Rays", "X-Rays"]},
                "ans": 1
            },
            {
                "hi": {"q": "काजीरंगा राष्ट्रीय उद्यान किस वन्यजीव के संरक्षण के लिए जाना जाता है?", "options": ["बंगाल टाइगर", "एक सींग वाला गैंडा", "एशियाई हाथी", "हिम तेंदुआ"]},
                "en": {"q": "Kaziranga National Park is famed for conserving which animal?", "options": ["Bengal Tiger", "One-horned Rhinoceros", "Asian Elephant", "Snow Leopard"]},
                "ans": 1
            },
            {
                "hi": {"q": "पृथ्वी की सतह का लगभग कितना भाग जल से आच्छादित है?", "options": ["लगभग 50%", "लगभग 71%", "लगभग 80%", "लगभग 60%"]},
                "en": {"q": "Approximately what percentage of Earth's surface is water?", "options": ["About 50%", "About 71%", "About 80%", "About 60%"]},
                "ans": 1
            },
            {
                "hi": {"q": "प्रसिद्ध चिपको आंदोलन किसकी रक्षा के लिए शुरू हुआ था?", "options": ["पशुओं की", "वनों के पेड़ों की", "नदियों की", "पहाड़ों की"]},
                "en": {"q": "The Chipko Movement was initiated to protect what?", "options": ["Animals", "Forest Trees", "Rivers", "Mountains"]},
                "ans": 1
            },
            {
                "hi": {"q": "सुंदरबन का मैंग्रोव वन मुख्य रूप से किस राज्य में स्थित है?", "options": ["ओडिशा", "पश्चिम बंगाल", "आंध्र प्रदेश", "तमिलनाडु"]},
                "en": {"q": "The Sundarbans mangrove forest is situated in which state?", "options": ["Odisha", "West Bengal", "Andhra Pradesh", "Tamil Nadu"]},
                "ans": 1
            },
            {
                "hi": {"q": "ग्लोबल वार्मिंग के लिए मुख्य ग्रीनहाउस गैस कौन सी मानी जाती है?", "options": ["कार्बन डाइऑक्साइड", "आर्गन", "हीलियम", "नियॉन"]},
                "en": {"q": "Which gas is the leading driver of the greenhouse effect?", "options": ["Carbon Dioxide", "Argon", "Helium", "Neon"]},
                "ans": 0
            },
            {
                "hi": {"q": "साइलेंट वैली नेशनल पार्क भारत के किस राज्य में स्थित है?", "options": ["कर्नाटक", "केरल", "उत्तराखंड", "असम"]},
                "en": {"q": "In which state is Silent Valley National Park located?", "options": ["Karnataka", "Kerala", "Uttarakhand", "Assam"]},
                "ans": 1
            },
            {
                "hi": {"q": "भारत में बाघों के संरक्षण के लिए 'प्रोजेक्ट टाइगर' कब शुरू हुआ?", "options": ["1973", "1980", "1965", "1992"]},
                "en": {"q": "In which year was Project Tiger launched in India?", "options": ["1973", "1980", "1965", "1992"]},
                "ans": 0
            },
            {
                "hi": {"q": "पृथ्वी पर पाया जाने वाला सबसे विशालकाय स्तनपायी प्राणी कौन सा है?", "options": ["अफ्रीकी हाथी", "ब्लू व्हेल", "जिराफ", "विशाल ऑक्टोपस"]},
                "en": {"q": "Which is the largest living mammal on Earth?", "options": ["African Elephant", "Blue Whale", "Giraffe", "Giant Octopus"]},
                "ans": 1
            }
        ]
    },
    10: {
        "title_hi": "सेट 10: कॉस्मिक ग्रैंड फिनाले",
        "title_en": "Set 10: Cosmic Grand Finale",
        "questions": [
            {
                "hi": {"q": "अंतरिक्ष की कक्षा में भेजा गया पहला जीवित प्राणी कौन सा था?", "options": ["अल्बर्ट बंदर", "लाइका नाम की कुतिया", "हैम चिंपांजी", "फेलिसिट बिल्ली"]},
                "en": {"q": "Who was the first living animal launched into Earth orbit?", "options": ["Albert the monkey", "Laika the dog", "Ham the chimpanzee", "Felicette the cat"]},
                "ans": 1
            },
            {
                "hi": {"q": "विश्व का सबसे ऊंचा जलप्रपात एंजेल फॉल्स किस देश में स्थित है?", "options": ["ब्राजील", "वेनेजुएला", "अमेरिका", "कोलंबिया"]},
                "en": {"q": "Angel Falls, the highest waterfall, is in which country?", "options": ["Brazil", "Venezuela", "USA", "Colombia"]},
                "ans": 1
            },
            {
                "hi": {"q": "कोलकाता से पहले ब्रिटिश भारत की वास्तविक राजधानी कौन सी थी?", "options": ["मुर्शिदाबाद", "कलकत्ता ही थी", "दिल्ली", "आगरा"]},
                "en": {"q": "Before Calcutta, which town was the regional company headquarters?", "options": ["Murshidabad", "Calcutta itself", "Delhi", "Agra"]},
                "ans": 1
            },
            {
                "hi": {"q": "भारतीय संविधान की मूल हस्तलिखित प्रति किस गैस के बॉक्स में सुरक्षित है?", "options": ["नाइट्रोजन", "हीलियम गैस", "आर्गन गैस", "ऑक्सीजन"]},
                "en": {"q": "Original copies of the Indian Constitution are preserved in which gas?", "options": ["Nitrogen", "Helium", "Argon", "Oxygen"]},
                "ans": 1
            },
            {
                "hi": {"q": "भारत में पहली बार ईवीएम का परीक्षण किस राज्य के चुनाव में हुआ?", "options": ["केरल", "गोवा", "कर्नाटक", "तमिलनाडु"]},
                "en": {"q": "In which state were EVMs first piloted in India?", "options": ["Kerala", "Goa", "Karnataka", "Tamil Nadu"]},
                "ans": 0
            },
            {
                "hi": {"q": "अंटार्कटिका में भारत का पहला स्थायी शोध केंद्र कौन सा था?", "options": ["मैत्री", "दक्षिण गंगोत्री", "भारती", "हिमाद्री"]},
                "en": {"q": "Which was India's first permanent base station in Antarctica?", "options": ["Maitri", "Dakshin Gangotri", "Bharati", "Himadri"]},
                "ans": 1
            },
            {
                "hi": {"q": "विश्व में किस संप्रभु देश का लिखित संविधान सबसे लंबा है?", "options": ["अमेरिका", "भारत", "ब्रिटेन", "ऑस्ट्रेलिया"]},
                "en": {"q": "Which sovereign nation holds the longest written constitution?", "options": ["USA", "India", "United Kingdom", "Australia"]},
                "ans": 1
            },
            {
                "hi": {"q": "राष्ट्रगान 'जन गण मन' को पूर्ण रूप से गाने का आधिकारिक समय क्या है?", "options": ["48 सेकंड", "52 सेकंड", "60 सेकंड", "55 सेकंड"]},
                "en": {"q": "What is the official playing time of the full National Anthem of India?", "options": ["48 Seconds", "52 Seconds", "60 Seconds", "55 Seconds"]},
                "ans": 1
            },
            {
                "hi": {"q": "प्राचीन भारत में शल्य चिकित्सा (प्लास्टिक सर्जरी) के जनक कौन थे?", "options": ["महर्षि चरक", "महर्षि सुश्रुत", "धन्वंतरि", "जीवक"]},
                "en": {"q": "Who is revered as the ancient Father of Plastic Surgery?", "options": ["Charaka", "Sushruta", "Dhanvantari", "Jivaka"]},
                "ans": 1
            },
            {
                "hi": {"q": "अंतर्राष्ट्रीय न्यायालय (ICJ) का प्रधान कार्यालय किस शहर में है?", "options": ["जिनेवा", "द हेग (नीदरलैंड)", "न्यूयॉर्क", "वियना"]},
                "en": {"q": "Where is the seat of the International Court of Justice located?", "options": ["Geneva", "The Hague (Netherlands)", "New York", "Vienna"]},
                "ans": 1
            }
        ]
    }
}
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>KHELO - Brain Arena</title>
    <style>
        :root {
            --neon-blue: #00f0ff;
            --neon-pink: #f72585;
            --neon-gold: #ffbe0b;
            --neon-green: #05ffa1;
            --bg-deep: #030712;
            --card-bg: rgba(15, 23, 42, 0.88);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            background-color: var(--bg-deep);
            background-image: 
                radial-gradient(at 0% 0%, rgba(114, 9, 183, 0.28) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(0, 240, 255, 0.22) 0px, transparent 50%),
                radial-gradient(at 50% 100%, rgba(247, 37, 133, 0.18) 0px, transparent 50%);
            color: #f8fafc;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 14px;
        }

        .arena-container {
            width: 100%;
            max-width: 580px;
            background: var(--card-bg);
            border: 1.5px solid rgba(0, 240, 255, 0.35);
            border-radius: 28px;
            box-shadow: 0 0 35px rgba(0, 240, 255, 0.18);
            padding: 20px;
            backdrop-filter: blur(14px);
        }

        /* Top Bar */
        .top-nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            background: rgba(8, 14, 29, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.12);
            padding: 8px 12px;
            border-radius: 18px;
        }

        .nav-actions {
            display: flex;
            gap: 8px;
            align-items: center;
        }

        .nav-btn {
            background: #111e3b;
            border: 1px solid rgba(255, 255, 255, 0.18);
            color: white;
            padding: 7px 12px;
            border-radius: 12px;
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
        }

        .nav-btn:hover {
            border-color: var(--neon-blue);
        }

        .btn-pause-toggle {
            border-color: var(--neon-pink);
            color: #fbcfe8;
        }

        .lang-switch {
            display: flex;
            background: #090e1e;
            border: 1px solid #1e293b;
            border-radius: 14px;
            padding: 2px;
        }

        .lang-btn {
            background: transparent;
            border: none;
            color: #94a3b8;
            font-size: 12px;
            font-weight: 700;
            padding: 5px 11px;
            border-radius: 10px;
            cursor: pointer;
        }

        .lang-btn.active {
            background: var(--neon-blue);
            color: #030712;
            box-shadow: 0 0 8px var(--neon-blue);
        }

        .timer-box {
            width: 42px;
            height: 42px;
            border-radius: 50%;
            border: 3px solid var(--neon-blue);
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 17px;
            font-weight: 900;
            color: var(--neon-blue);
        }

        .timer-danger {
            border-color: var(--neon-pink) !important;
            color: var(--neon-pink) !important;
            animation: pulse 0.7s infinite alternate;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            100% { transform: scale(1.1); }
        }

        /* IQ Power & Streak */
        .iq-grid-bar {
            background: linear-gradient(90deg, rgba(114, 9, 183, 0.35), rgba(0, 240, 255, 0.35));
            border: 1px solid var(--neon-blue);
            border-radius: 16px;
            padding: 12px 14px;
            margin-bottom: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .iq-badge {
            font-size: 20px;
            font-weight: 900;
            color: var(--neon-gold);
        }

        .rank-label {
            font-size: 12px;
            color: #cbd5e1;
            font-weight: 600;
        }

        .streak-chip {
            background: #090e1e;
            border: 1px solid #334155;
            padding: 4px 10px;
            border-radius: 16px;
            font-size: 12px;
            font-weight: 800;
            color: var(--neon-green);
        }

        /* Lifelines */
        .lifeline-row {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 16px;
        }

        .btn-life {
            background: #0f172a;
            border: 1px solid var(--neon-gold);
            color: var(--neon-gold);
            border-radius: 20px;
            padding: 7px 14px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
        }

        .btn-life:disabled {
            opacity: 0.35;
            cursor: not-allowed;
            border-color: #475569;
            color: #64748b;
        }

        /* Question Box */
        .question-box {
            background: #0b1329;
            border: 1.5px solid var(--neon-blue);
            border-radius: 18px;
            padding: 20px 16px;
            margin-bottom: 18px;
            text-align: center;
            position: relative;
        }

        .speaker-btn {
            position: absolute;
            top: 10px;
            right: 12px;
            background: rgba(0, 240, 255, 0.15);
            border: 1px solid var(--neon-blue);
            border-radius: 50%;
            width: 32px;
            height: 32px;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            font-size: 15px;
        }

        .question-title {
            font-size: 18px;
            font-weight: 700;
            line-height: 1.5;
            color: #ffffff;
            padding: 0 14px;
        }

        /* Options */
        .options-list {
            display: grid;
            grid-template-columns: 1fr;
            gap: 10px;
            margin-bottom: 16px;
        }
        .opt-card {
            background: rgba(15, 23, 42, 0.85);
            border: 1.5px solid #233458;
            border-radius: 14px;
            color: #f1f5f9;
            padding: 14px 16px;
            font-size: 15px;
            font-weight: 600;
            text-align: left;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 12px;
            transition: all 0.15s ease;
        }

        .opt-card:hover:not(:disabled) {
            border-color: var(--neon-blue);
            background: rgba(0, 240, 255, 0.08);
        }

        .opt-tag {
            width: 26px;
            height: 26px;
            border-radius: 8px;
            background: #1e293b;
            color: var(--neon-blue);
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 13px;
            font-weight: 800;
        }

        .opt-card.locked {
            background: #d97706 !important;
            border-color: #fef08a !important;
            color: #ffffff !important;
        }

        .opt-card.correct {
            background: rgba(5, 255, 161, 0.3) !important;
            border-color: var(--neon-green) !important;
            color: var(--neon-green) !important;
            box-shadow: 0 0 15px rgba(5, 255, 161, 0.4);
        }

        .opt-card.wrong {
            background: rgba(247, 37, 133, 0.3) !important;
            border-color: var(--neon-pink) !important;
            color: #fda4af !important;
            box-shadow: 0 0 15px rgba(247, 37, 133, 0.4);
        }

        .opt-card.hidden-50 {
            visibility: hidden;
            pointer-events: none;
        }

        /* Next Button */
        .btn-next {
            width: 100%;
            background: linear-gradient(90deg, var(--neon-blue), #7209b7);
            color: white;
            padding: 14px;
            border-radius: 14px;
            border: none;
            font-size: 16px;
            font-weight: 800;
            cursor: pointer;
            display: none;
            box-shadow: 0 0 18px rgba(0, 240, 255, 0.35);
        }

        /* Sets Grid */
        .sets-menu-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 14px;
            max-height: 450px;
            overflow-y: auto;
        }

        .set-btn {
            background: #090e21;
            border: 1.5px solid #1e293b;
            color: white;
            padding: 14px 10px;
            border-radius: 16px;
            cursor: pointer;
            text-align: center;
            font-size: 13px;
            transition: all 0.2s;
        }

        .set-btn.unlocked:hover {
            border-color: var(--neon-blue);
            transform: translateY(-2px);
        }

        .set-btn.locked {
            opacity: 0.4;
            cursor: not-allowed;
            background: #050814;
        }

        /* Modal Overlays */
        .modal-screen {
            display: none;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(3, 7, 18, 0.88);
            justify-content: center;
            align-items: center;
            z-index: 999;
            padding: 16px;
            backdrop-filter: blur(8px);
        }

        .modal-card {
            background: #0b1329;
            border: 1.5px solid var(--neon-blue);
            border-radius: 24px;
            padding: 24px;
            width: 100%;
            max-width: 380px;
            text-align: center;
        }
    </style>
</head>
<body>

<div class="arena-container">
    <!-- VIEW 1: Sets Selection -->
    <div id="view-sets">
        <div style="text-align: center; margin-bottom: 18px;">
            <h1 style="color:var(--neon-blue); font-size:32px; letter-spacing:3px; text-shadow:0 0 20px var(--neon-blue);">👑 KHELO</h1>
            <p style="color:#94a3b8; font-size:13px; margin-top:4px;" id="sets-subtitle">10 प्रगतिशील स्तर • बोलती आवाज के साथ</p>
        </div>
        <div class="sets-menu-grid" id="grid-sets"></div>
    </div>

    <!-- VIEW 2: Active Arena -->
    <div id="view-arena" style="display: none;">
        <!-- Top Nav Bar -->
        <div class="top-nav">
            <div class="nav-actions">
                <button class="nav-btn" onclick="goToHome()" title="Home">🏠 Home</button>
                <button class="nav-btn btn-pause-toggle" id="btn-pause" onclick="togglePause()">⏸️ Pause</button>
            </div>

            <div class="lang-switch">
                <button class="lang-btn active" id="btn-lang-hi" onclick="setLanguage('hi')">हिंदी</button>
                <button class="lang-btn" id="btn-lang-en" onclick="setLanguage('en')">English</button>
            </div>

            <div class="timer-box" id="hud-timer">30</div>
        </div>

        <!-- IQ Power & Rank Grid -->
        <div class="iq-grid-bar">
            <div>
                <div class="iq-badge" id="hud-iq">80 IQ</div>
                <div class="rank-label" id="hud-rank">नौसिखिया विचारक 🥉</div>
            </div>
            <div style="text-align: right;">
                <div class="streak-chip" id="hud-streak">🔥 Streak: 0x</div>
                <div style="font-size: 11px; color:#94a3b8; margin-top: 3px;" id="hud-progress">Q 1/10</div>
            </div>
        </div>

        <!-- Lifelines Deck -->
        <div class="lifeline-row">
            <button class="btn-life" id="life-50" onclick="trigger5050()">50:50</button>
            <button class="btn-life" id="life-poll" onclick="triggerPoll()">👥 Audience</button>
            <button class="btn-life" id="life-flip" onclick="triggerFlip()">🔄 Flip</button>
        </div>

        <!-- Question Box -->
        <div class="question-box">
            <div class="speaker-btn" onclick="speakCurrentQuestion()" title="Replay Voice">🔊</div>
            <div class="question-title" id="hud-question">लोड हो रहा है...</div>
        </div>

        <!-- Options Container -->
        <div class="options-list" id="hud-options"></div>

        <button class="btn-next" id="btn-next-q" onclick="advanceNextQuestion()">अगला सवाल (Next Question) →</button>
    </div>

    <!-- VIEW 3: Results Screen -->
    <div id="view-result" style="display: none; text-align: center; padding: 20px 0;">
        <h2 id="result-headline" style="color:var(--neon-gold); font-size:26px; margin-bottom:8px;">स्तर समाप्त!</h2>
        <p style="color:#94a3b8; font-size:14px;" id="result-label-iq">आपका अंतिम ब्रेन स्कोर:</p>
        <div id="result-final-iq" style="font-size:36px; font-weight:900; color:var(--neon-green); margin:15px 0;">80 IQ</div>
        <p id="result-subtext" style="color:#cbd5e1; font-size:14px; margin-bottom:24px;"></p>
        <button class="btn-next" style="display:block; margin-bottom:10px;" onclick="replaySet()">फिर से खेलें 🔄</button>
        <button class="btn-next" style="display:block; background:#1e293b;" onclick="goToHome()">मुख्य पृष्ठ (Home) 🏠</button>
    </div>
</div>

<!-- Audience Poll Modal -->
<div class="modal-screen" id="modal-poll">
    <div class="modal-card">
        <h3 style="color:var(--neon-gold); margin-bottom:14px;" id="poll-title">📊 जनता की राय (Audience Consensus)</h3>
        <div style="display:flex; justify-content:space-around; align-items:flex-end; height:120px; border-bottom:2px solid #334155; padding-bottom:6px; margin-bottom:16px;" id="poll-bars-area"></div>
        <button class="btn-next" style="display:block;" onclick="closePoll()">वापस खेलें (Return)</button>
    </div>
</div>

<script>
    let currentLanguage = 'hi';
    let synth = window.speechSynthesis;
    let availableVoices = [];

    function populateVoices() {
        if (!synth) return;
        availableVoices = synth.getVoices();
    }
    populateVoices();
    if (speechSynthesis.onvoiceschanged !== undefined) {
        speechSynthesis.onvoiceschanged = populateVoices;
    }

    function stopVoice() {
        if (synth) synth.cancel();
    }

    function speakText(text, lang) {
        stopVoice();
        if (!synth) return;

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.92;
        utterance.pitch = 1.0;

        populateVoices();

        if (lang === 'hi') {
            utterance.lang = 'hi-IN';
            // Search specifically for Hindi Voice
            const hiVoice = availableVoices.find(v => 
                v.lang === 'hi-IN' || 
                v.lang.toLowerCase().includes('hi') ||
                v.name.toLowerCase().includes('hindi')
            );
            if (hiVoice) utterance.voice = hiVoice;
        } else {
            utterance.lang = 'en-US';
            const enVoice = availableVoices.find(v => 
                v.lang.startsWith('en')
            );
            if (enVoice) utterance.voice = enVoice;
        }

        synth.speak(utterance);
    }

    // Audio SFX Engine (Buzzer & Bells)
    let audioCtx = null;
    function ensureAudio() {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if (audioCtx.state === 'suspended') audioCtx.resume();
    }

    function playTone(freq, type, duration, vol=0.2) {
        try {
            ensureAudio();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = type;
            osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
            gain.gain.setValueAtTime(vol, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + duration);
        } catch(e) {}
    }

    function sndTick() { playTone(800, 'triangle', 0.04, 0.15); }
    function sndLock() { playTone(240, 'sawtooth', 0.25, 0.25); }
    function sndCorrect() {
        playTone(523, 'sine', 0.15, 0.2);
        setTimeout(() => playTone(659, 'sine', 0.18, 0.2), 140);
        setTimeout(() => playTone(784, 'triangle', 0.35, 0.25), 280);
    }
    function sndWrong() { playTone(130, 'sawtooth', 0.5, 0.3); }

    // State Variables
    let activeSetId = 1;
    let timerRef = null;
    let timeLeft = 30;
    let isPaused = false;
    let isLocked = false;
    let questionData = null;
    let streakCount = 0;
    let lifelines = { fiftyFifty: true, poll: true, flip: true };

    function setLanguage(lang) {
        currentLanguage = lang;
        document.getElementById('btn-lang-hi').classList.toggle('active', lang === 'hi');
        document.getElementById('btn-lang-en').classList.toggle('active', lang === 'en');

        // Update titles
        if (document.getElementById('view-sets').style.display !== 'none') {
            loadSetsList();
            document.getElementById('sets-subtitle').innerText = (lang === 'hi') ? 
                "10 प्रगतिशील स्तर • बोलती आवाज के साथ" : 
                "10 Progressive Levels • Voice Assisted";
        }

        if (questionData && !isLocked) {
            updateQuestionDisplay();
            speakCurrentQuestion();
        }
    }

    function getMaxUnlockedLevel() {
        return parseInt(localStorage.getItem('khelo_iq_unlocked') || '1');
    }
    function setMaxUnlockedLevel(lvl) {
        const cur = getMaxUnlockedLevel();
        if (lvl > cur) localStorage.setItem('khelo_iq_unlocked', lvl.toString());
    }

    async function loadSetsList() {
        const res = await fetch('/api/get-sets');
        const sets = await res.json();
        const grid = document.getElementById('grid-sets');
        grid.innerHTML = '';
        const maxUnlocked = getMaxUnlockedLevel();

        sets.forEach(s => {
            const btn = document.createElement('button');
            const isUnlocked = s.id <= maxUnlocked;
            const title = (currentLanguage === 'hi') ? s.title_hi : s.title_en;
            const statusTxt = isUnlocked ? 
                ((currentLanguage === 'hi') ? 'अनलॉक' : 'UNLOCKED') : 
                ((currentLanguage === 'hi') ? 'लॉक' : 'LOCKED');

            btn.className = `set-btn ${isUnlocked ? 'unlocked' : 'locked'}`;
            btn.innerHTML = `
                <strong>${isUnlocked ? '🔓' : '🔒'} Set ${s.id}</strong><br>
                <span style="font-size:11px; opacity:0.85;">${title.split(':')[1] || title}</span><br>
                <span style="font-size:10px; color:${isUnlocked ? 'var(--neon-green)' : '#f87171'}; font-weight:700;">
                    ${statusTxt}
                </span>
            `;
            if (isUnlocked) {
                btn.onclick = () => launchSet(s.id);
            } else {
                btn.onclick = () => alert(
                    (currentLanguage === 'hi') ? 
                    `🔒 सेट ${s.id} लॉक है! कृपया पहले पिछले सेट को पूरा करें।` : 
                    `🔒 Set ${s.id} is locked! Clear previous sets first.`
                );
            }
            grid.appendChild(btn);
        });
    }
    async function launchSet(setId) {
        ensureAudio();
        stopVoice();
        activeSetId = setId;
        streakCount = 0;
        isPaused = false;
        isLocked = false;
        lifelines = { fiftyFifty: true, poll: true, flip: true };
        document.getElementById('life-50').disabled = false;
        document.getElementById('life-poll').disabled = false;
        document.getElementById('life-flip').disabled = false;
        document.getElementById('btn-pause').innerText = "⏸️ Pause";

        const res = await fetch('/api/start-set', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ set_id: setId })
        });

        if (res.ok) {
            document.getElementById('view-sets').style.display = 'none';
            document.getElementById('view-result').style.display = 'none';
            document.getElementById('view-arena').style.display = 'block';
            fetchNextQuestion();
        }
    }

    async function fetchNextQuestion() {
        clearInterval(timerRef);
        stopVoice();
        isLocked = false;
        isPaused = false;
        document.getElementById('btn-pause').innerText = "⏸️ Pause";
        document.getElementById('btn-next-q').style.display = 'none';

        const res = await fetch('/api/get-question');
        const data = await res.json();

        if (data.finished) {
            setMaxUnlockedLevel(activeSetId + 1);
            showResultView(true, data.won_iq, 
                (currentLanguage === 'hi') ? "बधाई हो! आपने इस सेट के सभी 10 प्रश्न पूरे कर लिए!" : "Congratulations! All 10 questions cleared!"
            );
            return;
        }

        questionData = data;
        document.getElementById('hud-progress').innerText = `Q ${data.q_index + 1}/10`;
        document.getElementById('hud-iq').innerText = data.iq;
        document.getElementById('hud-rank').innerText = (currentLanguage === 'hi') ? data.rank_hi : data.rank_en;
        document.getElementById('hud-streak').innerText = `🔥 Streak: ${streakCount}x`;

        updateQuestionDisplay();
        startTimer();
        speakCurrentQuestion();
    }

    function updateQuestionDisplay() {
        const langPack = (currentLanguage === 'hi') ? questionData.hi : questionData.en;
        document.getElementById('hud-question').innerText = `Q${questionData.q_index + 1}. ${langPack.q}`;
        renderOptions(langPack.options);
    }

    function speakCurrentQuestion() {
        if (isPaused) return;
        const langPack = (currentLanguage === 'hi') ? questionData.hi : questionData.en;
        speakText(langPack.q, currentLanguage);
    }

    function renderOptions(options) {
        const container = document.getElementById('hud-options');
        container.innerHTML = '';
        const prefixes = ["A", "B", "C", "D"];

        options.forEach((opt, idx) => {
            const btn = document.createElement('button');
            btn.className = 'opt-card';
            btn.id = `opt-${idx}`;
            btn.innerHTML = `<span class="opt-tag">${prefixes[idx]}</span> <span>${opt}</span>`;
            btn.onclick = () => selectOption(idx, btn);
            container.appendChild(btn);
        });
    }

    function startTimer() {
        timeLeft = 30;
        const hud = document.getElementById('hud-timer');
        hud.innerText = timeLeft;
        hud.classList.remove('timer-danger');

        timerRef = setInterval(() => {
            if (!isPaused && !isLocked) {
                timeLeft--;
                hud.innerText = timeLeft;
                if (timeLeft <= 5) {
                    hud.classList.add('timer-danger');
                    sndTick();
                }
                if (timeLeft <= 0) {
                    clearInterval(timerRef);
                    timeExpired();
                }
            }
        }, 1000);
    }

    function togglePause() {
        if (isLocked) return;
        isPaused = !isPaused;
        const btn = document.getElementById('btn-pause');

        if (isPaused) {
            stopVoice();
            btn.innerText = "▶️ Resume";
            btn.style.borderColor = "var(--neon-green)";
            btn.style.color = "var(--neon-green)";
        } else {
            ensureAudio();
            btn.innerText = "⏸️ Pause";
            btn.style.borderColor = "var(--neon-pink)";
            btn.style.color = "#fbcfe8";
            speakCurrentQuestion();
        }
    }

    function goToHome() {
        clearInterval(timerRef);
        stopVoice();
        document.getElementById('view-arena').style.display = 'none';
        document.getElementById('view-result').style.display = 'none';
        document.getElementById('modal-poll').style.display = 'none';
        document.getElementById('view-sets').style.display = 'block';
        loadSetsList();
    }

    async function selectOption(selectedIdx, btn) {
        if (isLocked || isPaused) return;
        isLocked = true;
        clearInterval(timerRef);
        stopVoice();

        sndLock();
        btn.classList.add('locked');

        try {
            const res = await fetch('/api/check-answer', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ chosen: selectedIdx })
            });
            const result = await res.json();
            btn.classList.remove('locked');

            const prefixes = ["A", "B", "C", "D"];
            const correctOptLetter = prefixes[result.correct_ans];

            if (result.correct) {
                btn.classList.add('correct');
                sndCorrect();
                streakCount++;
                document.getElementById('hud-streak').innerText = `🔥 Streak: ${streakCount}x`;
                document.getElementById('btn-next-q').style.display = 'block';

                if (currentLanguage === 'hi') {
                    speakText("आपका जवाब बिल्कुल सही है। बहुत बढ़िया!", 'hi');
                } else {
                    speakText("Your answer is correct! Well done.", 'en');
                }

                if (questionData.q_index === 9) {
                    setMaxUnlockedLevel(activeSetId + 1);
                    setTimeout(() => {
                        showResultView(true, "180+ IQ", 
                            (currentLanguage === 'hi') ? "अद्भुत! आपने सभी 10 प्रश्नों को हल कर लिया।" : "Phenomenal! All 10 answers completed."
                        );
                    }, 1500);
                }
            } else {
                btn.classList.add('wrong');
                const rightBtn = document.getElementById(`opt-${result.correct_ans}`);
                if (rightBtn) rightBtn.classList.add('correct');
                sndWrong();
                streakCount = 0;

                if (currentLanguage === 'hi') {
                    speakText(`आपका जवाब गलत है। सही उत्तर ऑप्शन ${correctOptLetter} था।`, 'hi');
                } else {
                    speakText(`Your answer is incorrect! The correct answer was option ${correctOptLetter}.`, 'en');
                }

                setTimeout(() => {
                    showResultView(false, (currentLanguage === 'hi') ? result.safe_iq_hi : result.safe_iq_en, 
                        (currentLanguage === 'hi') ? "गलत उत्तर के कारण खेल समाप्त हुआ।" : "Set concluded due to incorrect answer."
                    );
                }, 2600);
            }
        } catch (err) {
            btn.classList.remove('locked');
            isLocked = false;
        }
    }

    function timeExpired() {
        isLocked = true;
        stopVoice();
        sndWrong();

        if (currentLanguage === 'hi') {
            speakText("समय समाप्त हो गया है! खेल यहीं रुकता है।", 'hi');
        } else {
            speakText("Time limit expired! Evaluation halted.", 'en');
        }

        fetch('/api/time-out', { method: 'POST' })
            .then(r => r.json())
            .then(res => {
                showResultView(false, (currentLanguage === 'hi') ? res.safe_iq_hi : res.safe_iq_en, 
                    (currentLanguage === 'hi') ? "समय समाप्त होने के कारण खेल रुका।" : "Time expired!"
                );
            });
    }

    // Lifeline: 50:50
    async function trigger5050() {
        if (!lifelines.fiftyFifty || isLocked || isPaused) return;
        lifelines.fiftyFifty = false;
        document.getElementById('life-50').disabled = true;

        const res = await fetch('/api/lifeline-5050');
        const data = await res.json();
        data.removed.forEach(idx => {
            const btn = document.getElementById(`opt-${idx}`);
            if (btn) btn.classList.add('hidden-50');
        });
    }

    // Lifeline: Audience Poll
    async function triggerPoll() {
        if (!lifelines.poll || isLocked || isPaused) return;
        lifelines.poll = false;
        document.getElementById('life-poll').disabled = true;

        const res = await fetch('/api/lifeline-poll');
        const data = await res.json();
        const area = document.getElementById('poll-bars-area');
        area.innerHTML = '';
        const prefixes = ["A", "B", "C", "D"];

        prefixes.forEach((pref, i) => {
            const pct = data.votes[i];
            const col = document.createElement('div');
            col.style.display = "flex";
            col.style.flexDirection = "column";
            col.style.alignItems = "center";
            col.style.gap = "4px";
            col.innerHTML = `
                <span style="font-size:11px; font-weight:700;">${pct}%</span>
                <div style="width:28px; background:linear-gradient(180deg, var(--neon-blue), #7209b7); border-radius:4px 4px 0 0; height:${pct * 0.9}px;"></div>
                <strong style="color:var(--neon-blue); font-size:12px;">${pref}</strong>
            `;
            area.appendChild(col);
        });

        document.getElementById('modal-poll').style.display = 'flex';
    }

    function closePoll() {
        document.getElementById('modal-poll').style.display = 'none';
    }

    // Lifeline: Flip
    async function triggerFlip() {
        if (!lifelines.flip || isLocked || isPaused) return;
        lifelines.flip = false;
        document.getElementById('life-flip').disabled = true;

        const res = await fetch('/api/lifeline-flip');
        const data = await res.json();

        questionData = data;
        updateQuestionDisplay();
        startTimer();
        speakCurrentQuestion();
    }

    function advanceNextQuestion() {
        fetchNextQuestion();
    }

    function showResultView(isWon, iq, msg) {
        clearInterval(timerRef);
        stopVoice();
        document.getElementById('view-arena').style.display = 'none';
        document.getElementById('view-result').style.display = 'block';

        document.getElementById('result-headline').innerText = isWon ? 
            ((currentLanguage === 'hi') ? "🌟 स्तर पूर्ण हुआ! 🌟" : "🌟 LEVEL CLEARED! 🌟") : 
            ((currentLanguage === 'hi') ? "खेल समाप्त!" : "Evaluation Over");
            
        document.getElementById('result-final-iq').innerText = iq;
        document.getElementById('result-subtext').innerText = msg;
    }

    function replaySet() {
        launchSet(activeSetId);
    }

    loadSetsList();
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/get-sets', methods=['GET'])
def get_sets():
    summary = []
    for s_id, s_data in KHELO_SETS.items():
        summary.append({
            "id": s_id,
            "title_hi": s_data["title_hi"],
            "title_en": s_data["title_en"],
            "total_questions": len(s_data["questions"])
        })
    return jsonify(summary)

@app.route('/api/start-set', methods=['POST'])
def start_set():
    data = request.get_json()
    set_id = int(data.get('set_id', 1))
    if set_id not in KHELO_SETS:
        return jsonify({"error": "Invalid set"}), 400

    session['set_id'] = set_id
    session['q_index'] = 0
    session['won_iq'] = "70 IQ"
    return jsonify({"status": "ready"})

@app.route('/api/get-question', methods=['GET'])
def get_question():
    set_id = session.get('set_id', 1)
    q_idx = session.get('q_index', 0)
    questions = KHELO_SETS.get(set_id, {}).get("questions", [])

    if q_idx >= len(questions):
        return jsonify({
            "finished": True,
            "won_iq": "180+ IQ (Legend)"
        })

    q = questions[q_idx]
    iq_info = IQ_LEVELS[q_idx]

    return jsonify({
        "finished": False,
        "q_index": q_idx,
        "hi": q["hi"],
        "en": q["en"],
        "iq": iq_info["iq"],
        "rank_hi": iq_info["rank_hi"],
        "rank_en": iq_info["rank_en"]
    })

@app.route('/api/check-answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    chosen = int(data.get('chosen', -1))

    set_id = session.get('set_id', 1)
    q_idx = session.get('q_index', 0)
    questions = KHELO_SETS.get(set_id, {}).get("questions", [])
    q = questions[q_idx]
    correct_ans = q["ans"]

    def calc_safe(idx):
        if idx >= 6:
            return ("145 IQ (सुरक्षित पड़ाव 2)", "145 IQ (Safe Checkpoint 2)")
        elif idx >= 3:
            return ("115 IQ (सुरक्षित पड़ाव 1)", "115 IQ (Safe Checkpoint 1)")
        else:
            return ("70 IQ (आधार)", "70 IQ (Base)")

    safe_hi, safe_en = calc_safe(q_idx)

    if chosen == correct_ans:
        session['won_iq'] = IQ_LEVELS[q_idx]["iq"]
        session['q_index'] = q_idx + 1
        return jsonify({
            "correct": True,
            "correct_ans": correct_ans,
            "won_iq": IQ_LEVELS[q_idx]["iq"]
        })
    else:
        return jsonify({
            "correct": False,
            "correct_ans": correct_ans,
            "safe_iq_hi": safe_hi,
            "safe_iq_en": safe_en
        })

@app.route('/api/time-out', methods=['POST'])
def time_out():
    q_idx = session.get('q_index', 0)
    if q_idx >= 6:
        safe_hi, safe_en = ("145 IQ", "145 IQ")
    elif q_idx >= 3:
        safe_hi, safe_en = ("115 IQ", "115 IQ")
    else:
        safe_hi, safe_en = ("70 IQ", "70 IQ")
    return jsonify({"safe_iq_hi": safe_hi, "safe_iq_en": safe_en})

@app.route('/api/lifeline-5050', methods=['GET'])
def lifeline_5050():
    set_id = session.get('set_id', 1)
    q_idx = session.get('q_index', 0)
    q = KHELO_SETS.get(set_id, {}).get("questions", [])[q_idx]
    correct_ans = q["ans"]

    wrong_indices = [i for i in range(4) if i != correct_ans]
    removed = random.sample(wrong_indices, 2)
    return jsonify({"removed": removed})

@app.route('/api/lifeline-poll', methods=['GET'])
def lifeline_poll():
    set_id = session.get('set_id', 1)
    q_idx = session.get('q_index', 0)
    q = KHELO_SETS.get(set_id, {}).get("questions", [])[q_idx]
    correct_ans = q["ans"]

    correct_pct = random.randint(65, 88)
    rem = 100 - correct_pct
    p1 = random.randint(0, rem)
    p2 = random.randint(0, rem - p1)
    p3 = rem - p1 - p2
    wrongs = [p1, p2, p3]
    random.shuffle(wrongs)

    votes = [0, 0, 0, 0]
    votes[correct_ans] = correct_pct
    w_idx = 0
    for i in range(4):
        if i != correct_ans:
            votes[i] = wrongs[w_idx]
            w_idx += 1

    return jsonify({"votes": votes})

@app.route('/api/lifeline-flip', methods=['GET'])
def lifeline_flip():
    flip_pool = [
        {
            "hi": {"q": "भारत के किस राज्य को 'देवभूमि' कहा जाता है?", "options": ["हिमाचल प्रदेश", "उत्तराखंड", "केरल", "सिक्किम"]},
            "en": {"q": "Which Indian state is famously called 'Devbhoomi'?", "options": ["Himachal Pradesh", "Uttarakhand", "Kerala", "Sikkim"]},
            "ans": 1
        },
        {
            "hi": {"q": "अंतरिक्ष में पौधा उगाने वाला पहला देश कौन सा था?", "options": ["अमेरिका", "रूस", "चीन", "भारत"]},
            "en": {"q": "Which country was the first to cultivate a plant in space?", "options": ["USA", "Russia", "China", "India"]},
            "ans": 1
        }
    ]
    replacement = random.choice(flip_pool)
    q_idx = session.get('q_index', 0)
    iq_info = IQ_LEVELS[q_idx]

    return jsonify({
        "q_index": q_idx,
        "hi": replacement["hi"],
        "en": replacement["en"],
        "iq": iq_info["iq"],
        "rank_hi": iq_info["rank_hi"],
        "rank_en": iq_info["rank_en"]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)