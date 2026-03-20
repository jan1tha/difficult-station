import csv
import json
import hashlib

eta_data = [
    ("COLOMBO RDHS", "COLOMBO", 0.8),
    ("HORANA DGH", "KALUTARA", 0.9),
    ("PIMBURA BH", "KALUTARA", 1.2),
    ("WARAKAGODA PMCU", "KALUTARA", 1.3),
    ("ANDIAMBALAMA PMCU", "GAMPAHA", 1.3),
    ("KALAGEDIHENA PMCU", "GAMPAHA", 1.2),
    ("NARISSA PMCU", "RATNAPURA", 1.5),
    ("MOLKAWA PMCU", "KALUTARA", 1.6),
    ("YATTAPATHA PMCU", "KALUTARA", 1.8),
    ("EHELIYAGODA BH", "RATNAPURA", 1.8),
    ("WARAKAPOLA BH", "KEGALLE", 1.4),
    ("MAWANELLA BH", "KEGALLE", 1.5),
    ("KARAWANELLA BH", "KEGALLE", 1.6),
    ("HALVITIGALA PMCU", "GALLE", 1.4),
    ("KEGALLE DGH", "KEGALLE", 1.8),
    ("KEGALLE RDHS", "KEGALLE", 1.8),
    ("BALAPITIYA BH", "GALLE", 2.0),
    ("BALAPITIVA BH", "GALLE", 2.0),
    ("ELPITIYA BH", "GALLE", 1.6),
    ("GALLE NATIONAL HOSPITAL", "GALLE", 2.0),
    ("GALLE ROHS", "GALLE", 2.0),
    ("HIKKADUWA DH", "GALLE", 2.0),
    ("FOR WOMEN", "GALLE", 2.0),
    ("POTHUPITIYA DH", "RATNAPURA", 2.2),
    ("RATHNAPURA TEACHING HOSPITAL", "RATNAPURA", 2.2),
    ("RATHNAPURA RDHS", "RATNAPURA", 2.2),
    ("KOLAMBAGEARA PMCU", "RATNAPURA", 2.3),
    ("PERADENIYA TEACHING HOSPITAL", "KANDY", 2.4),
    ("GAMPOLA BH", "KANDY", 2.4),
    ("DERANGALA PMCU", "MATARA", 2.3),
    ("ROTAMBA PMCU", "MATARA", 2.4),
    ("KIRINDA PUHULWELLA DH", "MATARA", 2.4),
    ("ALUPOLA DH", "RATNAPURA", 2.5),
    ("KANDY NATIONAL HOSPITAL", "KANDY", 2.5),
    ("MATARA DGH", "MATARA", 2.5),
    ("BELIATTE DH", "HAMBANTOTA", 2.6),
    ("BELIIATTE DH", "HAMBANTOTA", 2.6),
    ("KALAWANA BH", "RATNAPURA", 2.7),
    ("WALASMULLA BH", "HAMBANTOTA", 2.7),
    ("DAMBULLA BH", "MATALE", 3.0),
    ("MATALE DGH", "MATALE", 2.8),
    ("MATALE RDHS", "MATALE", 2.8),
    ("BERALIHERA PMCU", "HAMBANTOTA", 2.5),
    ("HAMBANTOTA DGH", "HAMBANTOTA", 2.8),
    ("PALLEGAMA DH", "MATARA", 3.0),
    ("RANNA DH", "HAMBANTOTA", 2.5),
    ("TANGALLE BH", "HAMBANTOTA", 2.8),
    ("MINUWANGETE PMCU", "KURUNEGALA", 2.5),
    ("KULIYAPITIYA TEACHING HOSPITAL", "KURUNEGALA", 2.5),
    ("PALAMKOTTE DH", "RATNAPURA", 2.8),
    ("THELDENIYA BH", "KANDY", 2.8),
    ("RAMBUKEWELA PMCU", "KANDY", 2.8),
    ("KAMBURUPITIYA BH", "MATARA", 2.8),
    ("DERANIYAGALA DH", "KEGALLE", 2.0),
    ("BELIGALA DH", "KEGALLE", 2.2),
    ("MAHAPALLEGAMA DH", "KEGALLE", 2.3),
    ("KIRIPORUWA WATTA (ERH) DH", "KEGALLE", 2.4),
    ("MARAMBA DH", "MATARA", 2.6),
    ("DENIYAYA BH", "MATARA", 3.2),
    ("LANKAGAMA PMCU", "GALLE", 2.8),
    ("UDUGAMA BH", "GALLE", 2.8),
    ("UDUGAMA 8H", "GALLE", 2.8),
    ("NELUWA DH", "GALLE", 2.8),
    ("CHILAW DGH", "PUTTALAM", 2.5),
    ("MARAWILA BH", "PUTTALAM", 2.3),
    ("THISSAMAHARAMAYA BH", "HAMBANTOTA", 3.0),
    ("DAMBADENIYA BH", "KURUNEGALA", 2.8),
    ("KURUNEGALA TEACHING HOSPITAL", "KURUNEGALA", 2.8),
    ("KEKUNAGALLA PMCU", "KURUNEGALA", 2.9),
    ("WESTHALL DH", "KANDY", 3.0),
    ("NIKAWERATIYA BH", "KURUNEGALA", 3.0),
    ("KATUPOTHA DH", "KURUNEGALA", 3.0),
    ("PUTTALAM BH", "PUTTALAM", 3.0),
    ("TPUTTALAM BH", "PUTTALAM", 3.0),
    ("PUTTALAM CHEST", "PUTTALAM", 3.0),
    ("RAMBODA KOTMALE DH", "NUWARA ELIYA", 3.1),
    ("PAHALAGIRIBAWA DH", "KURUNEGALA", 3.1),
    ("ANDIYAGALA DH", "ANURADHAPURA", 3.1),
    ("DICKOYA BH", "NUWARA ELIYA", 3.0),
    ("KOTAGALA DH", "NUWARA ELIYA", 3.0),
    ("LINDULA DH", "NUWARA ELIYA", 3.2),
    ("NUWARA ELIYA DGH", "NUWARA ELIYA", 3.2),
    ("MORAHENA DH", "KANDY", 3.2),
    ("MENIKHINNA DH", "KANDY", 2.9),
    ("KOLONGODA DH", "KANDY", 3.3),
    ("KAHAWATTA BH", "RATNAPURA", 3.0),
    ("USGALA SIYABALANGAMUWA PMCU", "KURUNEGALA", 3.2),
    ("GALGAMUWA BH", "KURUNEGALA", 3.2),
    ("RIKILLAGASKADA BH", "NUWARA ELIYA", 3.3),
    ("YATAWATHTHA DH", "MATALE", 3.3),
    ("URUBOKKA DH", "MATARA", 3.2),
    ("PATTIYAGAMA PALLEGAMA DH", "KANDY", 3.2),
    ("ANURADHAPURA TEACHING HOSPITAL", "ANURADHAPURA", 3.8),
    ("ANURADHAPURA RDHS", "ANURADHAPURA", 3.8),
    ("KEKIRAWA BH", "ANURADHAPURA", 3.5),
    ("HABARANA DH", "ANURADHAPURA", 3.3),
    ("MAHAGIRILLA DH", "KURUNEGALA", 3.2),
    ("RAJANGANAYA DH", "KURUNEGALA", 3.5),
    ("ALUTHWEWA PMCU", "MATALE", 3.5),
    ("OPALGALA PMCU", "MATALE", 3.5),
    ("WALAPANE DH", "NUWARA ELIYA", 3.5),
    ("GONAPITIYA DH", "NUWARA ELIYA", 3.6),
    ("AGARAPATHANA DH", "NUWARA ELIYA", 3.6),
    ("NORTH MEDAKUMBURA DH", "NUWARA ELIYA", 3.5),
    ("SANGARAJAPURA DH", "KANDY", 3.4),
    ("MAHIYANGANAYA BH", "BADULLA", 3.5),
    ("WELIMADA BH", "BADULLA", 3.5),
    ("DAMBETENNA DH", "BADULLA", 3.5),
    ("ANAWILUNDAWA DH", "PUTTALAM", 3.2),
    ("KOTTUKACHCHIYA DH", "PUTTALAM", 3.5),
    ("MUNDALAMA MOH", "PUTTALAM", 3.2),
    ("NIKAWEWA DH", "KURUNEGALA", 3.5),
    ("UDAGAMA ATABAGE DH", "KANDY", 3.5),
    ("GALPIHILLA DH", "KANDY", 3.5),
    ("BANDARAWELA BH", "BADULLA", 3.7),
    ("HAMBEGAMUWA DH", "MONERAGALA", 3.8),
    ("MULOYA DH", "NUWARA ELIYA", 3.8),
    ("UPCOT PMCU", "NUWARA ELIYA", 3.8),
    ("GLANMORE DH", "BADULLA", 3.8),
    ("KEPPETIPOLA PMCU", "BADULLA", 3.8),
    ("LAGGALA PALLEGAMA MOH", "MATALE", 4.0),
    ("BADULLA TEACHING HOSPITAL", "BADULLA", 3.8),
    ("NOCHCHIYAGAMA DH", "ANURADHAPURA", 4.0),
    ("THAMBUTTEGAMA BH", "ANURADHAPURA", 4.0),
    ("GALNEWA DH", "ANURADHAPURA", 3.8),
    ("AYAGAMA DH", "RATNAPURA", 3.2),
    ("WELKENIYAYA PMCU", "RATNAPURA", 3.0),
    ("EMBILIPITIYA DGH", "RATNAPURA", 3.5),
    ("WANATHAWILLUWA DH", "PUTTALAM", 3.5),
    ("DAYAGAMA WEST DH", "NUWARA ELIYA", 4.0),
    ("RIDEEMALIYADDA MOH", "BADULLA", 4.0),
    ("UVA PARANAGAMA DH", "BADULLA", 4.0),
    ("DIYATHALAWA BH", "BADULLA", 3.8),
    ("POLONNARUWA DGH", "POLONNARUWA", 4.0),
    ("POLONNARUWA RDHS", "POLONNARUWA", 4.0),
    ("POLONNARUWA RENAL HOSPITAL", "POLONNARUWA", 4.0),
    ("BIBILE BH", "MONERAGALA", 4.2),
    ("KATHARAGAMA DH", "MONERAGALA", 4.0),
    ("BUTHTHALA DH", "MONERAGALA", 4.2),
    ("GIRANDURUKOTTE DH", "BADULLA", 4.2),
    ("ATHTHANAKADAWALA DH", "POLONNARUWA", 4.2),
    ("PULASTHIGAMA (BOP 400) DH", "POLONNARUWA", 4.2),
    ("MEEMURE PMCU", "KANDY", 4.6),
    ("NADUMGAMUWA DH", "BADULLA", 4.3),
    ("THENNAPANGUWA PMCU", "BADULLA", 4.4),
    ("THANTIRIMALE DH", "ANURADHAPURA", 4.3),
    ("MEDIRIGIRIYA BH", "POLONNARUWA", 4.3),
    ("SEVANAPITIYA PMCU", "POLONNARUWA", 4.3),
    ("ARALAGANWILA DH", "POLONNARUWA", 4.5),
    ("DIMBULAGALA MANAMPITIYA DH", "POLONNARUWA", 4.5),
    ("PADAVIYA BH", "ANURADHAPURA", 4.5),
    ("WAHALKADA DH", "ANURADHAPURA", 4.5),
    ("HATTOTA AMUNA DH", "MATALE", 4.5),
    ("MARAKA DH", "MATALE", 4.5),
    ("MONERAGALA DGH", "MONERAGALA", 4.5),
    ("MONERAGALA RDHS", "MONERAGALA", 4.5),
    ("RUPAHA PMCU", "NUWARA ELIYA", 4.2),
    ("KALAGANWATTA PMCU", "NUWARA ELIYA", 4.5),
    ("AAMBAGAHAPELESSA DH", "KANDY", 5.0),
    ("BATUMULLA DH", "KANDY", 4.9),
    ("LUNUGALA DH", "BADULLA", 4.2),
    ("SIYAMBALANDUWA BH", "MONERAGALA", 5.0),
    ("AMPARA DGH", "AMPARA", 5.5),
    ("AMPARA RDHS", "AMPARA", 5.5),
    ("DEHIATTAKANDIYA BH", "AMPARA", 5.0),
    ("MAHAOYA BH", "AMPARA", 5.5),
    ("PADIYATALAWA DH", "AMPARA", 5.5),
    ("KANTALE BH", "TRINCOMALEE", 4.8),
    ("KANTALE 8H", "TRINCOMALEE", 4.8),
    ("KUNCHUKULAM PMCU", "ANURADHAPURA", 5.4),
    ("KOTIYAGALA PMCU", "MONERAGALA", 5.5),
    ("INGINIYAGALA DH", "MONERAGALA", 5.5),
    ("VANKALAI DH", "MANNAR", 5.5),
    ("MURUNKAN BH", "MANNAR", 5.4),
    ("NEDUNKERNY DH", "VAVUNIYA", 5.7),
    ("WELIOYA MOH", "MULLAITIVU", 5.5),
    ("SERUWILA DH", "TRINCOMALEE", 5.2),
    ("GOMARANKADAWELA DH", "TRINCOMALEE", 5.5),
    ("TRINCOMALEE DGH", "TRINCOMALEE", 5.5),
    ("VAVUNIYA DGH", "VAVUNIYA", 5.5),
    ("IVAVUNIYA DGH", "VAVUNIYA", 5.5),
    ("IVAVUNIYA RDHS", "VAVUNIYA", 5.5),
    ("VAVUNIYA RDHS", "VAVUNIYA", 5.5),
    ("CHEDDIKULAM BH", "VAVUNIYA", 5.8),
    ("ECHCHANKULAM PMCU", "VAVUNIYA", 5.8),
    ("NERIYAKULAM DH", "VAVUNIYA", 5.9),
    ("MANNAR DGH", "MANNAR", 6.0),
    ("MANNAR RDHS", "MANNAR", 6.0),
    ("TAMPITIYA PMCU", "AMPARA", 5.8),
    ("VIDATHALTIVU DH", "MANNAR", 5.9),
    ("PERIYAMADHU PMCU", "MANNAR", 5.9),
    ("MANALCHENAI PMCU", "TRINCOMALEE", 6.0),
    ("PADAVISIRIPURA DH", "TRINCOMALEE", 6.0),
    ("KILIVETTY DH", "TRINCOMALEE", 6.0),
    ("KILIVETTY OH", "TRINCOMALEE", 6.0),
    ("MUTHUR BH", "TRINCOMALEE", 6.0),
    ("PULMODAI BH", "TRINCOMALEE", 6.0),
    ("KINNIYABH", "TRINCOMALEE", 5.5),
    ("THARAPURAM PMCU", "MANNAR", 6.0),
    ("POONAKERY DH", "KILINOCHCHI", 6.2),
    ("POONAKERY POONARYN DH", "KILINOCHCHI", 6.2),
    ("THALAIMANNAR DH", "MANNAR", 6.1),
    ("ERUKALAMPIDDY DH", "MANNAR", 6.2),
    ("SAMPOOR DH", "TRINCOMALEE", 6.2),
    ("MANKULAM BH", "MULLAITIVU", 6.0),
    ("NADDANKANDAL DH", "MULLAITIVU", 6.0),
    ("NANDANKANNDAL DH", "MULLAITIVU", 6.0),
    ("SENARATHPURA DH", "AMPARA", 6.5),
    ("ISENARATHPURA DH", "AMPARA", 6.5),
    ("LAHUGALA MOH", "AMPARA", 6.5),
    ("WEERAGODA PMCU", "AMPARA", 6.5),
    ("IRAKKAMAM DH", "KALMUNAI", 6.5),
    ("IRAKKAMAM ERAGAMA DH", "KALMUNAI", 6.5),
    ("VALAICHCHENAI BH", "BATTICALOA", 6.0),
    ("VALAICHCHENA! BH", "BATTICALOA", 6.0),
    ("CHENKALADY DH", "BATTICALOA", 6.2),
    ("KATHIRAVELY DH", "BATTICALOA", 6.3),
    ("MALLAVI BH", "MULLAITIVU", 6.2),
    ("KILINOCHCHI DGH", "KILINOCHCHI", 6.2),
    ("PALAI DH", "KILINOCHCHI", 6.3),
    ("THUNUKKAI PMCU", "MULLAITIVU", 6.3),
    ("ERAVUR BH", "BATTICALOA", 6.3),
    ("KALMUNAI NORTH BH", "KALMUNAI", 6.5),
    ("KALUWANCHIKUDY BH", "BATTICALOA", 6.5),
    ("KATTANKUDY BH", "BATTICALOA", 6.5),
    ("ODDUSUDDAN DH", "MULLAITIVU", 6.5),
    ("MULLAITIVU DGH", "MULLAITIVU", 6.5),
    ("PALUGAMAM DH", "BATTICALOA", 6.5),
    ("HOSPITAL", "KALMUNAI", 7.0),
    ("BATTICALOA TEACHING HOSPITAL", "BATTICALOA", 6.5),
    ("MEERAVODAI DH", "BATTICALOA", 6.5),
    ("JAFFNA TEACHING HOSPITAL", "JAFFNA", 7.0),
    ("JAFFNA RDHS", "JAFFNA", 7.0),
    ("CHAVAKACHCHERI BH", "JAFFNA", 7.0),
    ("GURUNAGAR DH", "JAFFNA", 7.0),
    ("KODIKAMAM DH", "JAFFNA", 7.0),
    ("INUVIL PMCU", "JAFFNA", 7.0),
    ("KAYTS BH", "JAFFNA", 7.0),
    ("MULLIYAN PMCU", "JAFFNA", 6.7),
    ("DEEGAWAPIYA DH", "KALMUNAI", 7.0),
    ("ANNAMALAI DH", "KALMUNAI", 7.0),
    ("ULLAI PMCU", "KALMUNAI", 7.0),
    ("THIRUKKOVIL BH", "KALMUNAI", 7.0),
    ("AKKARAIPATTU BH", "KALMUNAI", 6.8),
    ("SAMMANTHURAI BH", "KALMUNAI", 6.8),
    ("SAMMANTHURA! MOH", "KALMUNAI", 6.8),
    ("MANDUR DH", "BATTICALOA", 6.7),
    ("MAVADIVAMBU VANTHARAMOOLAIDH", "BATTICALOA", 6.8),
    ("NINTAVUR BH", "KALMUNAI", 7.0),
    ("NAWALKADU DH", "BATTICALOA", 6.8),
    ("TELLIPPALAI BH", "JAFFNA", 7.2),
    ("TELLIPPALAI MOH", "JAFFNA", 7.2),
    ("KANKASANTHURAI PMCU", "JAFFNA", 7.5),
    ("POINT PEDRO BH", "JAFFNA", 7.5),
    ("POINT PEDRO PMCU", "JAFFNA", 7.5),
    ("THOLPURAM PMCU", "JAFFNA", 7.5),
    ("ALAMPIL DH", "MULLAITIVU", 7.0),
    ("PUTHUKKUDYIRUPPU BH", "MULLAITIVU", 7.0),
    ("POTTUVIL BH", "KALMUNAI", 7.5),
    ("PANAMA DH", "AMPARA", 7.5),
    ("ANALATIVU DH", "JAFFNA", 10.5),
    ("MANNAN DGH", "MANNAR", 6.0),
]

coords = {
    "NARISSA PMCU": (6.6167, 80.2167), "MOLKAWA PMCU": (6.6051, 80.2377),
    "YATTAPATHA PMCU": (6.4667, 80.2167), "POTHUPITIYA DH": (6.4634, 80.4307),
    "DERANGALA PMCU": (6.2167, 80.5667), "ALUPOLA DH": (6.7167, 80.6167),
    "HALVITIGALA PMCU": (6.2833, 80.3167), "ROTAMBA PMCU": (6.1833, 80.5833),
    "PALAMKOTTE DH": (6.3333, 80.6167), "BERALIHERA PMCU": (6.1667, 81.0167),
    "AGARAPATHANA DH": (6.8641, 80.7056), "UPCOT PMCU": (6.7790, 80.6243),
    "WESTHALL DH": (7.0667, 80.5667), "RAJANGANAYA DH": (8.1657, 80.1964),
    "ALUTHWEWA PMCU": (8.0833, 80.9667), "OPALGALA PMCU": (7.5833, 80.7167),
    "USGALA SIYABALANGAMUWA PMCU": (8.0167, 80.3167), "DAYAGAMA WEST DH": (6.8548, 80.7586),
    "MORAHENA DH": (7.2167, 80.6833), "ANDIYAGALA DH": (7.9005, 80.5272),
    "PAHALAGIRIBAWA DH": (7.9833, 80.3500), "LANKAGAMA PMCU": (6.3333, 80.4667),
    "HAMBEGAMUWA DH": (6.5406, 80.9419), "GONAPITIYA DH": (7.0333, 80.7333),
    "NORTH MEDAKUMBURA DH": (6.9967, 80.6359), "MULOYA DH": (7.0667, 80.7667),
    "MEEMURE PMCU": (7.4333, 80.8333), "HATTOTA AMUNA DH": (7.6833, 80.8500),
    "KALAGANWATTA PMCU": (7.1000, 80.9000), "RUPAHA PMCU": (7.0500, 80.8500),
    "AAMBAGAHAPELESSA DH": (7.2722, 80.9833), "BATUMULLA DH": (7.4170, 80.9330),
    "THANTIRIMALE DH": (8.3500, 80.3833), "KOTIYAGALA PMCU": (6.7726, 81.5297),
    "KUNCHUKULAM PMCU": (8.8333, 80.0500), "MURUNKAN BH": (8.8326, 80.0324),
    "MARAKA DH": (7.5833, 80.9667), "WAHALKADA DH": (8.5667, 80.6222),
    "SERUWILA DH": (8.3708, 81.3193), "PERIYAMADHU PMCU": (9.0182, 80.1706),
    "VANKALAI DH": (8.8922, 79.9352), "WELIOYA MOH": (9.0125, 80.7850),
    "GOMARANKADAWELA DH": (8.7333, 80.9833), "MANALCHENAI PMCU": (8.5167, 81.1833),
    "PADAVISIRIPURA DH": (8.9367, 80.8133), "NEDUNKERNY DH": (9.1167, 80.5333),
    "ERUKALAMPIDDY DH": (9.1167, 79.8333), "THARAPURAM PMCU": (9.05, 79.85),
    "VIDATHALTIVU DH": (9.0333, 79.9833), "MALLAVI BH": (9.1333, 80.2833),
    "THUNUKKAI PMCU": (9.1500, 80.2167), "INGINIYAGALA DH": (7.2138, 81.5432),
    "ODDUSUDDAN DH": (9.1519, 80.6493), "POONAKERY DH": (9.5000, 80.2000),
    "POONAKERY POONARYN DH": (9.5000, 80.2000),
    "NAWALKADU DH": (7.7167, 81.6833), "MANDUR DH": (7.5167, 81.7333),
    "PALUGAMAM DH": (7.5333, 81.7167), "ALAMPIL DH": (9.1500, 80.8500),
    "PUTHUKKUDYIRUPPU BH": (9.3167, 80.7167), "SAMPOOR DH": (8.4833, 81.2833),
    "THALAIMANNAR DH": (9.0834, 79.7344), "KATHIRAVELY DH": (8.1167, 81.3833),
    "MULLIYAN PMCU": (9.5414, 80.4722), "KAYTS BH": (9.6667, 79.9833),
    "KILIVETTY DH": (8.5833, 81.2167), "KILIVETTY OH": (8.5833, 81.2167),
    "NADDANKANDAL DH": (9.2167, 80.5167), "NANDANKANNDAL DH": (9.2167, 80.5167),
    "SENARATHPURA DH": (7.2912, 81.6724), "ISENARATHPURA DH": (7.2912, 81.6724),
    "LAHUGALA MOH": (6.8781, 81.7200), "WEERAGODA PMCU": (7.3830, 81.6968),
    "DEEGAWAPIYA DH": (7.2842, 81.7867), "TAMPITIYA PMCU": (7.4167, 81.4833),
    "ANNAMALAI DH": (7.4500, 81.7833), "IRAKKAMAM DH": (7.2500, 81.7167),
    "IRAKKAMAM ERAGAMA DH": (7.2500, 81.7167), "ULLAI PMCU": (6.8417, 81.8333),
    "THIRUKKOVIL BH": (7.1150, 81.8519), "PANAMA DH": (6.7500, 81.8000),
    "HOSPITAL": (7.4199, 81.8228), "ANALATIVU DH": (9.6667, 79.7667),
    "COLOMBO RDHS": (6.9271, 79.8612),
    "HORANA DGH": (6.7167, 80.0667), "PIMBURA BH": (6.5500, 80.0500),
    "WARAKAGODA PMCU": (6.5833, 80.1500),
    "ANDIAMBALAMA PMCU": (7.2500, 79.9333), "KALAGEDIHENA PMCU": (7.1167, 80.0333),
    "RATHNAPURA TEACHING HOSPITAL": (6.6833, 80.4000), "RATHNAPURA RDHS": (6.6833, 80.4000),
    "EHELIYAGODA BH": (6.8333, 80.2333), "KOLAMBAGEARA PMCU": (6.6167, 80.3500),
    "BALANGODA BH": (6.6500, 80.6833), "KALAWANA BH": (6.5333, 80.3833),
    "KAHAWATTA BH": (6.5500, 80.7000), "EMBILIPITIYA DGH": (6.3500, 80.8500),
    "AYAGAMA DH": (6.4667, 80.3500), "WELKENIYAYA PMCU": (6.4500, 80.7500),
    "KEGALLE DGH": (7.2500, 80.3500), "KEGALLE RDHS": (7.2500, 80.3500),
    "MAWANELLA BH": (7.2500, 80.4500), "KARAWANELLA BH": (7.2667, 80.5167),
    "WARAKAPOLA BH": (7.1667, 80.3167), "DERANIYAGALA DH": (6.9167, 80.3333),
    "BELIGALA DH": (6.9333, 80.3833), "MAHAPALLEGAMA DH": (7.2167, 80.2833),
    "KIRIPORUWA WATTA (ERH) DH": (7.0667, 80.4500),
    "GALLE NATIONAL HOSPITAL": (6.0535, 80.2210), "GALLE ROHS": (6.0535, 80.2210),
    "ELPITIYA BH": (6.2833, 80.1667), "BALAPITIYA BH": (6.2667, 80.0167),
    "BALAPITIVA BH": (6.2667, 80.0167), "UDUGAMA BH": (6.3167, 80.3500),
    "UDUGAMA 8H": (6.3167, 80.3500), "HIKKADUWA DH": (6.1333, 80.1000),
    "NELUWA DH": (6.3833, 80.3167), "FOR WOMEN": (6.0400, 80.2350),
    "MATARA DGH": (5.9483, 80.5353), "DENIYAYA BH": (6.2167, 80.5833),
    "KAMBURUPITIYA BH": (5.9833, 80.4667), "KIRINDA PUHULWELLA DH": (6.0333, 80.5833),
    "MARAMBA DH": (5.9667, 80.5500), "PALLEGAMA DH": (6.1167, 80.6167),
    "URUBOKKA DH": (6.2333, 80.5333),
    "HAMBANTOTA DGH": (6.1219, 81.1194), "WALASMULLA BH": (6.0667, 80.8167),
    "BELIATTE DH": (6.0333, 80.7667), "TANGALLE BH": (6.0167, 80.7833),
    "RANNA DH": (6.0500, 80.9000), "THISSAMAHARAMAYA BH": (6.2833, 81.2833),
    "KANDY NATIONAL HOSPITAL": (7.2906, 80.6337), "PERADENIYA TEACHING HOSPITAL": (7.2667, 80.5833),
    "GAMPOLA BH": (7.1667, 80.5667), "THELDENIYA BH": (7.3167, 80.7500),
    "MENIKHINNA DH": (7.3667, 80.6500), "PATTIYAGAMA PALLEGAMA DH": (7.4500, 80.6333),
    "SANGARAJAPURA DH": (7.4333, 80.7167), "UDAGAMA ATABAGE DH": (7.5333, 80.7667),
    "KOLONGODA DH": (7.1667, 80.6000), "GALPIHILLA DH": (7.4333, 80.8500),
    "RAMBUKEWELA PMCU": (7.2500, 80.6667), "UDUNUWARA MOH": (7.3000, 80.5333),
    "DAMBULLA BH": (7.8667, 80.6500), "MATALE DGH": (7.4667, 80.6233),
    "MATALE RDHS": (7.4667, 80.6233), "YATAWATHTHA DH": (7.5333, 80.7500),
    "LAGGALA PALLEGAMA MOH": (7.5500, 80.7833),
    "NUWARA ELIYA DGH": (6.9708, 80.7831), "DICKOYA BH": (6.9333, 80.5833),
    "LINDULA DH": (6.9000, 80.5333), "KOTAGALA DH": (6.9167, 80.5167),
    "RIKILLAGASKADA BH": (7.0167, 80.6667), "RAMBODA KOTMALE DH": (7.0667, 80.6833),
    "WALAPANE DH": (7.0167, 80.7333),
    "BADULLA TEACHING HOSPITAL": (6.9833, 81.0553), "BANDARAWELA BH": (6.8333, 80.9833),
    "WELIMADA BH": (6.9000, 80.9167), "GIRANDURUKOTTE DH": (7.8167, 81.1833),
    "MAHIYANGANAYA BH": (7.3167, 81.0000), "DIYATHALAWA BH": (6.8000, 81.0167),
    "DAMBETENNA DH": (6.7667, 80.8667), "UVA PARANAGAMA DH": (6.8833, 81.1000),
    "LUNUGALA DH": (7.0167, 81.1333), "GLANMORE DH": (6.9167, 80.7500),
    "KEPPETIPOLA PMCU": (6.9167, 80.9333), "THENNAPANGUWA PMCU": (7.1000, 81.2333),
    "NADUMGAMUWA DH": (6.9000, 81.2000), "RIDEEMALIYADDA MOH": (7.1667, 81.3000),
    "MONERAGALA DGH": (6.8731, 81.3515), "MONERAGALA RDHS": (6.8731, 81.3515),
    "BIBILE BH": (7.1667, 81.2167), "KATHARAGAMA DH": (6.3833, 81.3333),
    "BUTHTHALA DH": (6.5667, 81.2167), "SIYAMBALANDUWA BH": (7.0833, 81.5333),
    "KURUNEGALA TEACHING HOSPITAL": (7.4833, 80.3667),
    "KULIYAPITIYA TEACHING HOSPITAL": (7.4667, 80.0500),
    "NIKAWERATIYA BH": (7.7333, 80.1167), "GALGAMUWA BH": (8.0167, 80.3167),
    "DAMBADENIYA BH": (7.4833, 80.2167), "KATUPOTHA DH": (7.5333, 80.4167),
    "KEKUNAGALLA PMCU": (7.5167, 80.3333), "MINUWANGETE PMCU": (7.3333, 80.2167),
    "MAHAGIRILLA DH": (7.8833, 80.4167), "NIKAWEWA DH": (8.1333, 80.2833),
    "CHILAW DGH": (7.5761, 79.7961), "PUTTALAM BH": (8.0333, 79.8333),
    "TPUTTALAM BH": (8.0333, 79.8333), "MARAWILA BH": (7.5000, 79.8500),
    "ANAWILUNDAWA DH": (8.0833, 79.8667), "KOTTUKACHCHIYA DH": (8.0000, 80.0000),
    "WANATHAWILLUWA DH": (8.3167, 79.9333), "MUNDALAMA MOH": (8.1500, 79.8000),
    "PUTTALAM CHEST": (8.0333, 79.8333),
    "ANURADHAPURA TEACHING HOSPITAL": (8.3500, 80.4000),
    "ANURADHAPURA RDHS": (8.3500, 80.4000), "KEKIRAWA BH": (8.0333, 80.6500),
    "HABARANA DH": (8.1833, 80.7500), "MEDAWACHCHIYA BH": (8.5500, 80.4833),
    "NOCHCHIYAGAMA DH": (8.2667, 80.2000), "GALNEWA DH": (8.2833, 80.3167),
    "PADAVIYA BH": (8.6500, 80.7833), "THAMBUTTEGAMA BH": (8.1167, 80.7167),
    "POLONNARUWA DGH": (7.9333, 81.0000), "POLONNARUWA RDHS": (7.9333, 81.0000),
    "POLONNARUWA RENAL HOSPITAL": (7.9333, 81.0050), "MEDIRIGIRIYA BH": (8.1000, 81.0500),
    "ARALAGANWILA DH": (7.2833, 81.0667), "ATHTHANAKADAWALA DH": (7.8833, 81.0333),
    "DIMBULAGALA MANAMPITIYA DH": (7.8833, 81.1333),
    "PULASTHIGAMA (BOP 400) DH": (7.9000, 81.1167), "SEVANAPITIYA PMCU": (7.9833, 81.1167),
    "AMPARA DGH": (7.3008, 81.6725), "AMPARA RDHS": (7.3008, 81.6725),
    "DEHIATTAKANDIYA BH": (7.7167, 81.3500), "MAHAOYA BH": (7.5167, 81.6500),
    "PADIYATALAWA DH": (7.5833, 81.5500),
    "AKKARAIPATTU BH": (7.2167, 81.8500), "KALMUNAI NORTH BH": (7.4167, 81.8333),
    "NINTAVUR BH": (7.3167, 81.8333), "POTTUVIL BH": (6.9500, 81.8333),
    "SAMMANTHURAI BH": (7.3667, 81.8167), "SAMMANTHURA! MOH": (7.3667, 81.8167),
    "BATTICALOA TEACHING HOSPITAL": (7.7167, 81.6972),
    "ERAVUR BH": (7.7667, 81.6667), "KALUWANCHIKUDY BH": (7.6667, 81.7167),
    "KATTANKUDY BH": (7.6833, 81.7333), "VALAICHCHENAI BH": (8.1000, 81.5167),
    "VALAICHCHENA! BH": (8.1000, 81.5167), "CHENKALADY DH": (7.9500, 81.6000),
    "MEERAVODAI DH": (7.7500, 81.7000),
    "MAVADIVAMBU VANTHARAMOOLAIDH": (8.0167, 81.5833),
    "TRINCOMALEE DGH": (8.5653, 81.2352), "KANTALE BH": (8.3833, 81.0167),
    "KANTALE 8H": (8.3833, 81.0167), "KINNIYABH": (8.5500, 81.2167),
    "MUTHUR BH": (8.4500, 81.2500), "PULMODAI BH": (8.9833, 81.2333),
    "VAVUNIYA DGH": (8.7500, 80.4987), "IVAVUNIYA DGH": (8.7500, 80.4987),
    "IVAVUNIYA RDHS": (8.7500, 80.4987), "VAVUNIYA RDHS": (8.7500, 80.4987),
    "CHEDDIKULAM BH": (9.0167, 80.3500), "ECHCHANKULAM PMCU": (9.0833, 80.4667),
    "NERIYAKULAM DH": (8.8667, 80.5167),
    "MANNAR DGH": (8.9826, 79.9030), "MANNAR RDHS": (8.9826, 79.9030),
    "MULLAITIVU DGH": (9.2667, 80.8167), "MANKULAM BH": (9.1333, 80.5000),
    "KILINOCHCHI DGH": (9.3833, 80.4000), "PALAI DH": (9.4667, 80.3167),
    "JAFFNA TEACHING HOSPITAL": (9.6681, 80.0169), "JAFFNA RDHS": (9.6681, 80.0169),
    "POINT PEDRO BH": (9.8167, 80.2333), "POINT PEDRO PMCU": (9.8167, 80.2333),
    "CHAVAKACHCHERI BH": (9.6500, 80.1667), "TELLIPPALAI BH": (9.7167, 80.0500),
    "TELLIPPALAI MOH": (9.7167, 80.0500), "GURUNAGAR DH": (9.6667, 80.0667),
    "KODIKAMAM DH": (9.6833, 80.1167), "KANKASANTHURAI PMCU": (9.7833, 80.0500),
    "INUVIL PMCU": (9.6833, 80.0167), "THOLPURAM PMCU": (9.6167, 80.4333),
    "BALANGODA BH": (6.6500, 80.6833),
}


def normalize_designation(raw):
    d = raw.strip().upper().replace('.', '').replace('[', '').replace('!', '').strip()
    if d in ('AMOH',):
        return 'AMOH'
    if d == 'MOIC':
        return 'MOIC'
    if 'RELIEF' in d:
        return 'MO Relief'
    if 'MENTAL HEALTH' in d:
        return 'MO Mental Health'
    if 'ANAESTHESIA' in d or 'ANESTHESIA' in d:
        return 'MO Anaesthesia / ICU'
    if 'BLOOD BANK' in d:
        return 'MO Blood Bank'
    if 'CARDIOLOGY' in d:
        return 'MO Cardiology'
    if 'DIALYSIS' in d:
        return 'MO Dialysis'
    if 'ENT' in d:
        return 'MO ENT'
    if 'EYE' in d or 'VITREO' in d or 'OPHTHAL' in d:
        return 'MO Eye'
    if 'GYN' in d or 'OBS' in d:
        return 'SHO GYN & OBS' if d.startswith('SHO') else 'MO GYN & OBS'
    if 'PICU' in d or 'NICU' in d or 'MICU' in d or 'SICU' in d:
        return 'MO ICU'
    if 'ICU' in d and 'NEURO' not in d:
        return 'MO Anaesthesia / ICU'
    if 'NEURO SURGERY' in d or 'NEUROLOGY' in d:
        return 'MO Neurology / Neurosurgery'
    if 'PBU' in d or 'SCBU' in d:
        return 'MO PBU / SCBU'
    if 'PAEDIATRIC SURGERY' in d:
        return 'MO Surgery'
    if 'PAEDIATRIC' in d or 'PAEDIATRICS' in d:
        return 'SHO Paediatrics' if d.startswith('SHO') else 'MO Paediatrics'
    if 'PATHOLOGY' in d or 'CHEMICAL PATH' in d or 'MICROBIOLOGY' in d or 'HAEMATOLOGY' in d:
        return 'MO Pathology / Lab'
    if 'PSYCHIATRY' in d:
        return 'MO Psychiatry'
    if 'RADIOLOGY' in d:
        return 'MO Radiology'
    if 'REHABILITATION' in d:
        return 'MO Rehabilitation'
    if 'ONCOL' in d or 'ONCO' in d:
        return 'MO Oncology'
    if 'ORTHO' in d:
        return 'MO Orthopaedic'
    if 'VASCULAR' in d or 'TRANSPLANT' in d:
        return 'MO Vascular Surgery'
    if 'PLASTIC' in d:
        return 'MO Surgery'
    if 'UROLOGY' in d or 'GU SURGERY' in d or 'GENITO' in d:
        return 'MO Urology / GU'
    if 'NEPHROLOGY' in d:
        return 'MO Nephrology'
    if 'ENDOCRINOLOGY' in d:
        return 'MO Endocrinology'
    if 'RHEUMATOLOGY' in d:
        return 'MO Rheumatology'
    if 'GASTRO' in d:
        return 'MO Gastroenterology'
    if 'RESPIRATORY' in d or 'PULMONOL' in d:
        return 'MO Respiratory'
    if 'DERMATOLOGY' in d:
        return 'MO Dermatology'
    if 'MEDICO LEGAL' in d:
        return 'MO Medico Legal'
    if 'STD' in d:
        return 'MO STD'
    if 'A&E' in d:
        return 'MO A&E'
    if 'ETU' in d or 'OPD' in d:
        return 'MO OPD / ETU'
    if 'SURGERY' in d and d.startswith('SHO'):
        return 'SHO Surgery'
    if 'MEDICINE' in d and d.startswith('SHO'):
        return 'SHO Medicine'
    if 'SURGERY' in d:
        return 'MO Surgery'
    if 'MEDICINE' in d:
        return 'MO Medicine'
    if 'SOE' in d:
        return 'MO (SOE)'
    if d.startswith('SHO'):
        return 'SHO'
    return 'MO'


def is_dh(institute):
    name = institute.strip().upper().replace('|', '').replace('[', '').replace(']', '').strip()
    return name.endswith(' DH') or name == 'DH'


def lookup_eta(clean_name, district):
    for e_name, e_dist, e_time in eta_data:
        if e_name == clean_name:
            return e_time
    for e_name, e_dist, e_time in eta_data:
        if e_name in clean_name or clean_name in e_name:
            return e_time
    fallback = {
        'JAFFNA': 7.0, 'MULLAITIVU': 6.5, 'KILINOCHCHI': 6.5,
        'MANNAR': 6.0, 'VAVUNIYA': 5.5,
        'BATTICALOA': 6.5, 'AMPARA': 6.0, 'KALMUNAI': 7.0,
        'TRINCOMALEE': 5.5, 'POLONNARUWA': 4.2,
        'ANURADHAPURA': 4.0, 'KURUNEGALA': 3.0,
        'BADULLA': 4.0, 'MONERAGALA': 5.0,
        'NUWARA ELIYA': 3.5, 'KANDY': 3.0, 'MATALE': 3.5,
        'RATNAPURA': 2.5, 'KEGALLE': 2.0,
        'HAMBANTOTA': 2.8, 'MATARA': 2.5, 'GALLE': 2.0,
        'KALUTARA': 1.5, 'GAMPAHA': 1.2, 'COLOMBO': 0.8,
        'PUTTALAM': 3.0,
    }
    return fallback.get(district, 5.0)


def lookup_coords(clean_name):
    if clean_name in coords:
        return coords[clean_name]
    for k, v in coords.items():
        if k in clean_name or clean_name in k:
            return v
    return None, None


def create_files():
    all_vacancies = []
    with open('Source/Vacancy List.csv', 'r') as f:
        for row in csv.DictReader(f):
            all_vacancies.append(row)

    difficult_indices = set()
    with open('AVAILABLE_DIFFICULT_STATIONS.csv', 'r') as f:
        for row in csv.DictReader(f):
            difficult_indices.add(row['INDEX'])

    stations = []
    for row in all_vacancies:
        inst = row['INSTITUTE'].strip().upper()
        clean_name = inst.replace('|', '').replace('_', '').replace('[', '').replace(']', '').strip()
        is_difficult = row['INDEX'] in difficult_indices
        eta = lookup_eta(clean_name, row['DISTRICT'])
        lat, lon = lookup_coords(clean_name)
        stations.append({
            "INDEX": row['INDEX'],
            "DISTRICT": row['DISTRICT'],
            "INSTITUTE": row['INSTITUTE'],
            "DESIGNATION": row['DESIGNATION'],
            "VACANCIES": row['VACANCIES'],
            "ESTIMATED_TRAVEL_TIME_HOURS": eta,
            "IS_DIFFICULT": "YES" if is_difficult else "NO",
            "IS_DH": "YES" if is_dh(row['INSTITUTE']) else "NO",
            "DESIG_GROUP": normalize_designation(row['DESIGNATION']),
            "lat": lat,
            "lon": lon
        })

    stations.sort(key=lambda x: x['ESTIMATED_TRAVEL_TIME_HOURS'])

    csv_fields = ['INDEX', 'DISTRICT', 'INSTITUTE', 'DESIGNATION', 'VACANCIES',
                  'ESTIMATED_TRAVEL_TIME_HOURS', 'IS_DIFFICULT', 'IS_DH', 'DESIG_GROUP']

    with open('ALL_STATIONS_BY_ETA.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        writer.writeheader()
        for s in stations:
            writer.writerow({k: s[k] for k in csv_fields})

    diff_stations = [s for s in stations if s['IS_DIFFICULT'] == 'YES']
    with open('DIFFICULT_STATIONS_BY_ETA.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['INDEX', 'DISTRICT', 'INSTITUTE', 'DESIGNATION',
                                               'VACANCIES', 'ESTIMATED_TRAVEL_TIME_HOURS', 'IS_DH', 'DESIG_GROUP'])
        writer.writeheader()
        for s in diff_stations:
            writer.writerow({k: s[k] for k in ['INDEX', 'DISTRICT', 'INSTITUTE', 'DESIGNATION',
                                                'VACANCIES', 'ESTIMATED_TRAVEL_TIME_HOURS', 'IS_DH', 'DESIG_GROUP']})

    non_diff = [s for s in stations if s['IS_DIFFICULT'] == 'NO']
    with open('NON_DIFFICULT_STATIONS.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['INDEX', 'DISTRICT', 'INSTITUTE', 'DESIGNATION',
                                               'VACANCIES', 'IS_DH', 'DESIG_GROUP'])
        writer.writeheader()
        for s in non_diff:
            writer.writerow({k: s[k] for k in ['INDEX', 'DISTRICT', 'INSTITUTE', 'DESIGNATION',
                                                'VACANCIES', 'IS_DH', 'DESIG_GROUP']})

    valid_markers = []
    for s in stations:
        if s['lat'] is not None:
            valid_markers.append({
                "name": s['INSTITUTE'],
                "district": s['DISTRICT'],
                "lat": s['lat'],
                "lon": s['lon'],
                "eta": s['ESTIMATED_TRAVEL_TIME_HOURS'],
                "vacancies": s['VACANCIES'],
                "designation": s['DESIGNATION'],
                "desig_group": s['DESIG_GROUP'],
                "is_difficult": s['IS_DIFFICULT'] == 'YES',
                "is_dh": is_dh(s['INSTITUTE'])
            })

    with open('markers.js', 'w') as f:
        f.write("var markersData = " + json.dumps(valid_markers) + ";")

    pwd_hash = hashlib.sha256("redda2026".encode()).hexdigest()
    diff_count = sum(1 for m in valid_markers if m['is_difficult'])
    non_diff_count = len(valid_markers) - diff_count
    no_coords = sum(1 for s in stations if s['lat'] is None)

    html = """<!DOCTYPE html>
<html>
<head>
    <title>Sri Lanka Medical Vacancies Map</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script src="markers.js"></script>
    <style>
        * { box-sizing: border-box; }
        body { margin: 0; padding: 0; font-family: Arial, sans-serif; }
        #map { height: 100vh; width: 100%%; display: none; }
        #login-overlay { position: fixed; top: 0; left: 0; width: 100%%; height: 100%%;
            background: #f0f2f5; display: flex; justify-content: center; align-items: center; z-index: 10000; }
        .login-box { background: white; padding: 30px; border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1); text-align: center; width: 300px; }
        .login-box h2 { margin-bottom: 20px; color: #1c1e21; }
        .login-box input { width: 100%%; padding: 12px; margin-bottom: 16px;
            border: 1px solid #dddfe2; border-radius: 6px; font-size: 16px; }
        .login-box button { width: 100%%; padding: 12px; background: #1877f2; color: white;
            border: none; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; }
        #error-msg { color: #d93025; font-size: 14px; margin-top: 10px; display: none; }
        #filter-panel { position: fixed; top: 10px; right: 10px; z-index: 1000;
            background: white; border-radius: 10px; box-shadow: 0 2px 12px rgba(0,0,0,0.2);
            width: 260px; display: none; }
        #filter-header { padding: 10px 14px; font-weight: bold; font-size: 14px;
            background: #1877f2; color: white; border-radius: 10px 10px 0 0;
            cursor: pointer; display: flex; justify-content: space-between; align-items: center; }
        #filter-body { padding: 12px 14px; }
        #filter-body.collapsed { display: none; }
        .filter-section { margin-bottom: 12px; }
        .filter-section label.section-label { font-size: 11px; font-weight: bold; color: #666;
            text-transform: uppercase; letter-spacing: 0.5px; display: block; margin-bottom: 6px; }
        .radio-group label { display: flex; align-items: center; gap: 6px;
            font-size: 13px; cursor: pointer; padding: 2px 0; }
        select.filter-select { width: 100%%; padding: 6px 8px; font-size: 13px;
            border: 1px solid #ddd; border-radius: 5px; }
        #filter-count { font-size: 12px; color: #555; text-align: center;
            padding: 6px 0 2px; border-top: 1px solid #eee; margin-top: 8px; }
        .reset-btn { width: 100%%; margin-top: 8px; padding: 6px; font-size: 12px;
            background: #f0f2f5; border: 1px solid #ddd; border-radius: 5px; cursor: pointer; }
        .reset-btn:hover { background: #e0e2e5; }
        .info.legend { line-height: 22px; font-size: 12px; padding: 8px 12px;
            background: white; border-radius: 6px; box-shadow: 0 1px 6px rgba(0,0,0,0.2); }
        .legend i { width: 12px; height: 12px; display: inline-block;
            margin-right: 5px; border-radius: 50%%; vertical-align: middle; }
    </style>
</head>
<body>
    <div id="login-overlay">
        <div class="login-box">
            <h2>Medical Vacancies Map</h2>
            <input type="password" id="password-input" placeholder="Enter password"
                   onkeydown="if(event.key==='Enter') checkPassword()">
            <button onclick="checkPassword()">Unlock Map</button>
            <p id="error-msg">Incorrect password!</p>
        </div>
    </div>
    <div id="filter-panel">
        <div id="filter-header" onclick="toggleFilters()">
            <span id="filter-toggle-label">&#9660; Filters</span>
            <span id="filter-count-badge" style="font-size:11px;font-weight:normal;"></span>
        </div>
        <div id="filter-body">
            <div class="filter-section">
                <label class="section-label">Station Type</label>
                <div class="radio-group">
                    <label><input type="radio" name="stype" value="all" checked onchange="applyFilters()"> All Stations</label>
                    <label><input type="radio" name="stype" value="difficult" onchange="applyFilters()"> Difficult only</label>
                    <label><input type="radio" name="stype" value="standard" onchange="applyFilters()"> Standard only</label>
                </div>
            </div>
            <div class="filter-section">
                <label class="section-label">Facility Type</label>
                <div class="radio-group">
                    <label><input type="radio" name="ftype" value="all" checked onchange="applyFilters()"> All</label>
                    <label><input type="radio" name="ftype" value="dh" onchange="applyFilters()"> DH only</label>
                    <label><input type="radio" name="ftype" value="nondh" onchange="applyFilters()"> Non-DH only</label>
                </div>
            </div>
            <div class="filter-section">
                <label class="section-label">Designation</label>
                <select id="desig-filter" class="filter-select" onchange="applyFilters()">
                    <option value="">All Designations</option>
                </select>
            </div>
            <div class="filter-section">
                <label class="section-label">District</label>
                <select id="district-filter" class="filter-select" onchange="applyFilters()">
                    <option value="">All Districts</option>
                </select>
            </div>
            <div id="filter-count"></div>
            <button class="reset-btn" onclick="resetFilters()">Reset Filters</button>
        </div>
    </div>
    <div id="map"></div>
    <script>
    function toggleFilters() {
        var body = document.getElementById('filter-body');
        var lbl = document.getElementById('filter-toggle-label');
        if (body.classList.contains('collapsed')) {
            body.classList.remove('collapsed');
            lbl.textContent = '\\u25BC Filters';
        } else {
            body.classList.add('collapsed');
            lbl.textContent = '\\u25B2 Filters';
        }
    }
    async function checkPassword() {
        const password = document.getElementById('password-input').value;
        const hashBuffer = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(password));
        const hashHex = Array.from(new Uint8Array(hashBuffer)).map(b => b.toString(16).padStart(2,'0')).join('');
        if (hashHex === '%(PWD_HASH)s') {
            document.getElementById('login-overlay').style.display = 'none';
            document.getElementById('map').style.display = 'block';
            document.getElementById('filter-panel').style.display = 'block';
            initMap();
        } else {
            document.getElementById('error-msg').style.display = 'block';
        }
    }
    var allMarkerLayers = [];
    var map;
    function etaColor(eta) {
        if (eta < 3) return '#27ae60';
        if (eta < 5) return '#e67e22';
        return '#e74c3c';
    }
    function initMap() {
        map = L.map('map').setView([7.8731, 80.7718], 7);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        var desigs = [...new Set(markersData.map(m => m.desig_group))].sort();
        var dsel = document.getElementById('desig-filter');
        desigs.forEach(function(d) {
            var opt = document.createElement('option');
            opt.value = d; opt.textContent = d; dsel.appendChild(opt);
        });
        var districts = [...new Set(markersData.map(m => m.district))].sort();
        var distsel = document.getElementById('district-filter');
        districts.forEach(function(d) {
            var opt = document.createElement('option');
            opt.value = d; opt.textContent = d; distsel.appendChild(opt);
        });

        markersData.forEach(function(m) {
            var color = etaColor(parseFloat(m.eta));
            var fillOpacity = m.is_difficult ? 0.75 : 0.2;
            var radius = m.is_dh ? 9 : 7;
            var dashArray = m.is_dh ? null : '4 3';
            var weight = m.is_difficult ? 2.5 : 1.5;
            var shape = L.circleMarker([m.lat, m.lon], {
                color: color, fillColor: color, fillOpacity: fillOpacity,
                radius: radius, weight: weight, dashArray: dashArray
            });
            var diffBadge = m.is_difficult
                ? ' <span style="background:#c0392b;color:white;padding:1px 5px;border-radius:3px;font-size:11px;">DIFFICULT</span>'
                : ' <span style="background:#7f8c8d;color:white;padding:1px 5px;border-radius:3px;font-size:11px;">STANDARD</span>';
            var dhBadge = m.is_dh
                ? ' <span style="background:#2980b9;color:white;padding:1px 5px;border-radius:3px;font-size:11px;">DH</span>'
                : '';
            shape.bindPopup(
                '<b>' + m.name + '</b>' + diffBadge + dhBadge +
                '<br>District: ' + m.district +
                '<br>Designation: ' + m.designation +
                ' <small style="color:#888;">(' + m.desig_group + ')</small>' +
                '<br>Vacancies: ' + m.vacancies +
                '<br>ETA from Homagama: <b>' + m.eta + ' hrs</b>'
            );
            allMarkerLayers.push({ layer: shape, data: m });
            shape.addTo(map);
        });

        var legend = L.control({ position: 'bottomright' });
        legend.onAdd = function() {
            var div = L.DomUtil.create('div', 'info legend');
            div.innerHTML =
                '<b>ETA from Homagama</b><br>' +
                '<i style="background:#27ae60"></i> &lt; 3 hrs<br>' +
                '<i style="background:#e67e22"></i> 3 &ndash; 5 hrs<br>' +
                '<i style="background:#e74c3c"></i> &gt; 5 hrs<br>' +
                '<hr style="margin:6px 0"><b>Station Type</b><br>' +
                '<span style="display:inline-block;width:12px;height:12px;border-radius:50%%;background:#888;opacity:0.75;margin-right:5px;vertical-align:middle;"></span>Difficult (filled)<br>' +
                '<span style="display:inline-block;width:12px;height:12px;border-radius:50%%;border:2px solid #888;opacity:0.8;margin-right:5px;vertical-align:middle;"></span>Standard (hollow)<br>' +
                '<hr style="margin:6px 0"><b>Facility</b><br>' +
                '<span style="display:inline-block;width:12px;height:12px;border-radius:50%%;background:#888;margin-right:5px;vertical-align:middle;"></span>DH (r=9)<br>' +
                '<span style="display:inline-block;width:10px;height:10px;border-radius:50%%;border:2px dashed #888;margin-right:5px;vertical-align:middle;"></span>Non-DH (dashed r=7)';
            return div;
        };
        legend.addTo(map);
        updateCount();
    }
    function applyFilters() {
        var stype = document.querySelector('input[name=stype]:checked').value;
        var ftype = document.querySelector('input[name=ftype]:checked').value;
        var desig = document.getElementById('desig-filter').value;
        var district = document.getElementById('district-filter').value;
        allMarkerLayers.forEach(function(ml) {
            var m = ml.data;
            var show = true;
            if (stype === 'difficult' && !m.is_difficult) show = false;
            if (stype === 'standard' && m.is_difficult) show = false;
            if (ftype === 'dh' && !m.is_dh) show = false;
            if (ftype === 'nondh' && m.is_dh) show = false;
            if (desig && m.desig_group !== desig) show = false;
            if (district && m.district !== district) show = false;
            if (show) { if (!map.hasLayer(ml.layer)) ml.layer.addTo(map); }
            else { if (map.hasLayer(ml.layer)) map.removeLayer(ml.layer); }
        });
        updateCount();
    }
    function resetFilters() {
        document.querySelector('input[name=stype][value=all]').checked = true;
        document.querySelector('input[name=ftype][value=all]').checked = true;
        document.getElementById('desig-filter').value = '';
        document.getElementById('district-filter').value = '';
        applyFilters();
    }
    function updateCount() {
        var visible = allMarkerLayers.filter(ml => map.hasLayer(ml.layer)).length;
        var total = allMarkerLayers.length;
        document.getElementById('filter-count').textContent = 'Showing ' + visible + ' of ' + total + ' vacancies';
        document.getElementById('filter-count-badge').textContent = visible + '/' + total;
    }
    </script>
</body>
</html>""" % {'PWD_HASH': pwd_hash}

    with open('index.html', 'w') as f:
        f.write(html)

    print(f"Files regenerated successfully.")
    print(f"  Total vacancies (source): {len(all_vacancies)}")
    print(f"  Markers on map: {len(valid_markers)} ({diff_count} difficult, {non_diff_count} standard)")
    print(f"  No coords (skipped from map): {no_coords}")
    print(f"  ALL_STATIONS_BY_ETA.csv: {len(stations)} rows")
    print(f"  DIFFICULT_STATIONS_BY_ETA.csv: {len(diff_stations)} rows")
    print(f"  NON_DIFFICULT_STATIONS.csv: {len(non_diff)} rows")


if __name__ == "__main__":
    create_files()
