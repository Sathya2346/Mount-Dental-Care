"""Default Mount Dental Care content used by the ``seed_demo`` command.

This module is the single source of truth for a fresh install:

* the CMS text content (site settings, nav, services, doctors, gallery,
  addresses, hours, footer links, page copy and hero banners)
* the bundled media in ``backend/seed_media/`` which is copied into ``MEDIA_ROOT``

Records are matched with a natural key (name/title/key/...), so re-running the
command is safe and never creates duplicates. Without ``--reset`` only missing
records are created and only blank fields are filled, which keeps whatever was
edited in Django Admin.
"""

import os
import shutil
from pathlib import Path

from django.conf import settings

from .models import (
    Award,
    Branch,
    ClinicAddress,
    ClinicHour,
    ClinicImage,
    Doctor,
    EmailTemplate,
    FooterLink,
    GalleryItem,
    HeroBanner,
    NavItem,
    OfferBanner,
    PageContent,
    Service,
    SiteSettings,
    SiteText,
    TrustFeature,
    YoutubeVideo,
)

SEED_MEDIA_DIR = Path(settings.BASE_DIR) / "seed_media"
# Drop folder for updated doctor photos. Whatever sits here replaces the matching
# bundled file in ``seed_media/doctors/``, so the seed data always carries the
# photos the clinic currently wants to show.
SAMPLE_MEDIA_DIR = Path(settings.PROJECT_ROOT) / "sample"

# --------------------------------------------------------------------------- #
# Site settings
# --------------------------------------------------------------------------- #

SITE_FIELDS = {
    "clinic_name": "Mount Dental Care",
    "email": "mountdentalcare@gmail.com",
    "logo": "site/logo.png",
    "hero_background_image": "site/hero-background.jpg",
    "hero_title": "Healthy Smiles, Lifelong Confidence",
    "hero_description": (
        "Looking for a dentist near me? Mount Dental Care is a trusted dental clinic "
        "in Chennai providing expert dental care and dental services with advanced "
        "technology and personalized treatment. From preventive care to dental implants, "
        "teeth whitening, braces and more, we provide compassionate care for the whole "
        "family, with same-day dental appointment slots available."
    ),
    "metric_dentists": "15+",
    "metric_equipment": "3D CBCT",
    "metric_emi": "0% EMI",
    "metric_patients": "5,000+",
    "topbar_hours": "Mon-Sat : Morning - 10.00 AM - 01.00 PM | Evening 05.00 PM - 08.30 PM",
    "whatsapp_number": "917010823417",
    "footer_about": (
        "Providing exceptional, patient-first dental treatments with cutting-edge "
        "technology and genuine human warmth. Your smile is our lifelong masterpiece."
    ),
    "footer_copyright": "© 2026 Mount Dental Care & Clinic. All rights reserved.",
}

NAV_ITEMS = [
    {"label": "Home", "sort_order": 0},
    {"label": "Why Choose Us", "sort_order": 1},
    {"label": "Our Dentists", "sort_order": 2},
    {"label": "About Clinic", "sort_order": 3},
    {"label": "Smile Gallery", "sort_order": 4},
    {"label": "Awards", "sort_order": 5},
]

OFFER = {
    "eyebrow": "ADVANCED DENTAL DIAGNOSTICS",
    "title": "3D CBCT Scan, Digital X-Ray & Intraoral Scan",
    "description": (
        "Get a complete picture of your oral health with our state-of-the-art diagnostic package. "
        "Our 3D CBCT Scan delivers high-precision volumetric imaging for implant planning and complex treatments, "
        "Digital X-Rays provide instant low-radiation tooth and bone assessment, and our Intraoral Camera Scan "
        "captures detailed images inside your mouth for accurate, comfortable diagnosis — all in one visit at Mount Dental Care, Chennai."
    ),
    "button_text": "Book Today",
}

SERVICES = [
    ("stethoscope", "General Dentistry",
     "Comprehensive oral exams, digital X-rays, cavity diagnostics, preventive care and routine dental check-ups for the whole family — the everyday foundation of quality family dentistry."),
    ("sparkles", "Teeth Cleaning & Polishing",
     "Gentle ultrasonic scaling and teeth cleaning to remove stubborn plaque and tartar buildup, helping keep your gums healthy and your smile fresh."),
    ("sun", "Teeth Whitening",
     "Advanced laser teeth whitening for a brighter, more confident smile. Our professional in-office treatment is designed to deliver noticeable results in a comfortable 45-minute visit."),
    ("activity", "Root Canal Treatment",
     "Microscope-assisted, comfortable root canal treatment performed by our in-house endodontist to help save natural teeth and restore comfortable function."),
    ("shield", "Dental Implants",
     "Restore missing teeth with titanium and zirconia dental implants designed for natural function, comfort and a confident smile. Options include single implants, All-on-4 and full-mouth implants."),
    ("layers", "Braces & Clear Aligners",
     "Personalized clear aligners, invisible aligners and discreet ceramic braces to straighten teeth, improve bite alignment and create a healthier, more confident smile for children, teens and adults."),
    ("smile", "Cosmetic Dentistry",
     "Transform your smile with custom porcelain veneers, composite resin veneers, aesthetic dental bonding and gummy smile contouring for natural-looking results."),
    ("baby", "Children's Dentistry",
     "Gentle, child-friendly pediatric dental care including dental check-ups, fluoride treatments and sealants for growing smiles."),
]

TRUST_FEATURES = [
    ("award", "Experienced Dental Specialists",
     "Endodontists, implantologists and pediatric dental specialists with over 21+ years of combined mastery."),
    ("cpu", "Advanced Dental Technology",
     "Equipped with 3D CBCT scanners, intraoral scanners and computer-guided laser dentistry for precise diagnosis and digital treatment planning."),
    ("feather", "Comfortable Procedures",
     "Gentle injection techniques, nitrous oxide sedation options and calming noise-cancelling headsets."),
    ("sparkle", "Hygienic Environment",
     "Hospital-grade 5-stage autoclave sterilization protocols, HEPA-filtered operatory suites and single-use kits."),
    ("clipboard", "Personalized Treatment Plans",
     "Transparent upfront cost estimates with no hidden fees, flexible treatment options and affordable dental care plans designed around your needs and budget."),
    ("bell", "Priority Dental Support",
     "Fast telephone assistance and priority scheduling for patients looking for a same-day dental appointment."),
]

DOCTORS = [
    {
        "name": "Dr. S. NATESH M.D.S.",
        "role": "Lead Dentist & Founder • Consultant Dental Surgeon, Endodontist & Implantologist • 21+ Years Experience",
        "image": "doctors/natesh.jpg",
        "bio": (
            "Dr. S. Natesh is a Consultant Dental Surgeon, Endodontist and Implantologist "
            "with 21+ years of clinical experience. He has extensive experience in "
            "endodontic care, implantology, veneers and digital smile design, including "
            "more than 3,000 dental implant placements."
        ),
        "education": "BDS, MDS",
        "expertise": "Implantology, Veneers, Digital Smile Design",
        "tenure": "21+ Years Active Clinical Practice",
        "memberships": "Indian Dental Association (IDA)",
        "is_lead": True,
        "sort_order": 0,
    },
    {
        "name": "Dr. N. PADMINI M.D.S.",
        "role": "Consultant Dental Surgeon & Orthodontist",
        "image": "doctors/padmini.jpg",
        "is_lead": False,
        "sort_order": 1,
    },
]

GALLERY = [
    {
        "title": "INTERVIEW",
        "description": "Interview of Dr. S. Natesh on SUN NEWS Satellite Television for DOCTOR'S NEWS on 9-9-2010 from 11AM to 12 NOON Live Programme.",
        "image": "gallery/interview-natesh-sun-news-2010.jpg",
        "sort_order": 0,
    },
    {
        "title": "INTERVIEW",
        "description": "Interview of Dr. A.S. Subhashini on SUN NEWS Satellite Television in \"Doctor Sun News\" Program held on March 2007 between 8:00pm - 9:00 pm.",
        "image": "gallery/interview-subhashini-doctor-sun-news-2007.jpg",
        "sort_order": 1,
    },
    {
        "title": "INTERVIEW",
        "description": "Interview of Dr. A.S. Subhashini on SUN NEWS Satellite Television for DOCTOR'S NEWS on 23.7.2010 from 11AM to 12 NOON Live Programme.",
        "image": "gallery/interview-subhashini-sun-news-2010.jpg",
        "sort_order": 2,
    },
    {
        "title": "INTERVIEW",
        "description": "Interview of Dr. Natesh on Makkal TV in Maruthuva Neram held on, 18-11-2009 between 3:00pm - 4:00pm.",
        "image": "gallery/interview-sun-news.jpg",
        "sort_order": 3,
    },
    {
        "title": "INTERVIEW",
        "description": "Interview of Dr. A.S. Subhashini on SUN NEWS Satellite Television in \"Doctor Sun News\" Program held on March 2008 between 8:00pm - 9:00 pm.",
        "image": "gallery/interview-subhashini-doctor-sun-news-2008.jpg",
        "sort_order": 4,
    },
    {
        "title": "SUN NEWS INTERVIEW",
        "description": "Interview of Dr. A.S. Subhashini on SUN NEWS Satellite Television for \"Doctor Sun News\" Programme held on March 2008 between 8:00pm - 9:00 pm.",
        "image": "gallery/interview-natesh-makkal-tv-2009.jpg",
        "sort_order": 5,
    },
]

# --------------------------------------------------------------------------- #
# Addresses and opening hours
# --------------------------------------------------------------------------- #

ADDRESSES = [
    "5/66–1A, Butt Road, St. Thomas Mount, Chennai 600016",
    "37/2, 1st Floor, Valluvar Kottam High Road, Nungambakkam, Chennai 600034",
]

HOURS = [
    ("Mon - Sat", "Morning - 10.00 AM - 01.00 PM | Evening 05.00 PM - 08.30 PM", False),
    ("St.Thomas Mount - 044-2234 5000", "Nungambakkam - 044-2827 5000", False),
]

FOOTER_LINKS = [
    ("quick", "About Our Clinic", "#about-clinic"),
    ("quick", "Our Doctors & Team", "#our-dentists"),
    ("quick", "Smile Gallery & Results", "#smile-gallery"),
    ("quick", "Why Choose Us", "#why-choose-us"),
    ("quick", "Awards & Recognitions", "#awards"),
    ("treatments", "Laser Teeth Whitening", "#services"),
    ("treatments", "Dental Implants (Titanium & Zirconia)", "#services"),
    ("treatments", "Clear Aligners & Braces", "#services"),
    ("treatments", "Comfortable Root Canal Treatment", "#services"),
    ("treatments", "Porcelain Cosmetic Veneers", "#services"),
    ("treatments", "Children’s Pediatric Care", "#services"),
]

PAGES = [
    ("why", "THE MOUNT DENTAL DIFFERENCE", "Why Patients Trust Mount Dental Care",
     "We believe visiting the dentist should be pleasant, relaxed and genuinely reassuring. Our patient-first approach combines experienced specialists, advanced technology and compassionate care to create an experience patients can trust."),
    ("about", "ABOUT MOUNT DENTAL CARE", "Setting the Standard for Compassionate, Modern Dentistry",
     "Founded with a passion to redefine dental anxiety into a soothing, empowering health journey, Mount Dental Care has grown into a trusted dental clinic in Chennai, providing comprehensive dental care for individuals and families. We combine modern dental technology, clinical expertise and a patient-first approach to provide comfortable, personalized care."),
    ("experts", "MEET OUR EXPERTS", "Led by Renowned Dental Specialists",
     "Our clinicians regularly train in Switzerland and the US in the latest micro-surgical and aesthetic protocols."),
    ("gallery", "VISUAL TOUR & RESULTS", "Our Smile Gallery & Clinic Experience",
     "Explore our sterile, welcoming clinic suites, real patient transformations and state-of-the-art facilities."),
    ("appointment", "EASY ONLINE BOOKING", "Schedule Your Smile Consultation",
     "Take the first step towards better oral health. Select your preferred date and treatment, and our patient coordinator will confirm your dental appointment within 15 minutes."),
    ("contact", "GET IN TOUCH", "We’d Love to Welcome You",
     "Conveniently located with dedicated patient parking, accessible transit links and friendly reception support for a comfortable visit."),
]

# Subject/body for every message the clinic sends. Both built-in template
# types are seeded so they appear in Admin (CMS -> Email Templates) and can be
# reworded there; a missing row falls back to the same copy in email_utils.
EMAIL_TEMPLATES = [
    (
        "appointment_otp",
        "Your Mount Dental Care verification code is {{otp}}",
        "Hello {{full_name}},\n\nYour Mount Dental Care appointment verification code is: {{otp}}\n\nThis code expires in {{expiry_minutes}} minutes. Do not share this code with anyone.\n\nAppointment date: {{preferred_date}}\nTreatment: {{treatment_type}}\n\nMount Dental Care",
    ),
    (
        "admin_appointment_notify",
        "New Appointment Booking - {{full_name}} ({{treatment_type}})",
        "A new appointment has been booked on Mount Dental Care.\n\n--- Patient Details ---\nName: {{full_name}}\nMobile: {{mobile_number}}\nEmail: {{email}}\nPreferred Date: {{preferred_date}}\nTreatment: {{treatment_type}}\nMessage: {{message}}\n\nBooked at: {{booked_at}}\nAppointment ID: {{appointment_id}}\n\nPlease log in to the admin panel to review and confirm this appointment.\n\n-- Mount Dental Care System",
    ),
]

HERO_BANNERS = [
    ("Advanced Dental Technology", "image", "hero-banners/clinic-equipment.jpeg", 0),
    ("3D CBCT Diagnostic Imaging", "image", "hero-banners/cbct-scan.jpeg", 1),
    ("Modern Dental Clinic", "image", "hero-banners/dental-clinic.jpg", 2),
    ("Clinic Tour", "video", "hero-banners/clinic-tour.mp4", 3),
    ("Dental Technology Tour", "video", "hero-banners/technology-tour.mp4", 4),
]

BANNER_TITLES = {title for title, _type, _media, _order in HERO_BANNERS}

# --------------------------------------------------------------------------- #
# Service "Learn More" popups
# --------------------------------------------------------------------------- #

# Keyed by the service title used in SERVICES above, so a fresh install ships
# with the full detail panel. Every field is editable (or blank) in Admin.
SERVICE_DETAILS = {
    "General Dentistry": {
        "badge": "PREVENTIVE & DIAGNOSTIC CARE",
        "full_description": "General dentistry forms the foundation of lifelong oral wellness for every member of your family. Our comprehensive consultations combine gentle physical exams, high-resolution digital intraoral cameras, and low-radiation digital radiography to detect early signs of decay, gum inflammation, and enamel wear long before they develop into complex dental issues.",
        "highlights": [
            "Digital oral health evaluation and computerized cavity detection",
            "Low-radiation digital radiography & intraoral photo documentation",
            "Biocompatible tooth-colored composite restorations (aesthetic fillings)",
            "Preventive fluoride enamel applications & diagnostic bite analysis",
            "Customized home oral hygiene roadmap and dietary guidance",
        ],
    },
    "Teeth Cleaning & Polishing": {
        "badge": "HYGIENE & GUM WELLNESS",
        "full_description": "Professional dental prophylaxis is essential for removing stubborn bacterial plaque and calcified tartar deposits that regular brushing cannot reach. Our clinicians utilize state-of-the-art ultrasonic scalers with fine micro-water sprays to gently dislodge calculus from tooth surfaces and below the gumline, followed by diamond-paste polishing that restores silky-smooth enamel luster.",
        "highlights": [
            "Advanced gentle ultrasonic scaling to eliminate calculus and plaque",
            "Subgingival cleaning to prevent gingivitis and periodontal disease",
            "Enamel polishing with specialized prophy paste for stain removal",
            "Removal of stubborn coffee, tea, and food surface discolorations",
            "Antiseptic gum soothing treatment for refreshed, healthy gums",
        ],
    },
    "Teeth Whitening": {
        "badge": "AESTHETIC ENAMEL BRIGHTENING",
        "full_description": "Restore natural luminosity to your smile with our professional in-office laser teeth whitening system. Unlike abrasive over-the-counter kits, our clinical procedure uses a pH-balanced whitening formulation activated by targeted cool-light laser technology. This lifts deep enamel and dentin stains while strictly shielding your gums and maintaining tooth comfort.",
        "highlights": [
            "Up to 6 to 8 shades lighter in a single, relaxed clinical session",
            "Protective light-cured gingival barrier to safeguard delicate gums",
            "Controlled cool LED laser activation for optimal oxidation and stain breakdown",
            "Specialized post-whitening potassium nitrate desensitizing treatment",
            "Long-lasting, radiant results with comprehensive aftercare instructions",
        ],
    },
    "Root Canal Treatment": {
        "badge": "MICROSCOPE-ASSISTED ENDODONTICS",
        "full_description": "When deep decay, cracks, or trauma reach the tooth's innermost nerve chamber, modern endodontic therapy saves the natural tooth and relieves acute discomfort. Utilizing high-magnification dental operating microscopes and computerized digital apex locators, our specialist cleans, disinfects, and hermetically seals the root canal anatomy with biocompatible gutta-percha, allowing you to chew with comfort and confidence.",
        "highlights": [
            "Computer-guided local anesthesia for a genuinely comfortable experience",
            "Microscope-assisted precision visualization of micro-canal branches",
            "Flexible nickel-titanium rotary file instrumentation for thorough cleaning",
            "Biocompatible hermetic seal to prevent reinfection and promote healing",
            "Custom crown preparation to restore structural strength and natural aesthetics",
        ],
    },
    "Dental Implants": {
        "badge": "PERMANENT TOOTH RESTORATION",
        "full_description": "Dental implants represent the modern gold standard for replacing missing teeth. An implant consists of a medical-grade titanium or zirconia post that integrates directly with the alveolar bone, mimicking a natural tooth root. Topped with a custom handcrafted ceramic crown, implants prevent bone loss, restore 100% bite functionality, and blend seamlessly with your surrounding natural teeth.",
        "highlights": [
            "3D CBCT volumetric bone scan and virtual computer-guided planning",
            "Biocompatible titanium or metal-free ceramic zirconia implant fixtures",
            "Preserves natural jawbone density and youthful facial contours",
            "No alteration or shaving down of adjacent healthy teeth required",
            "Versatile solutions from single tooth replacement to full-arch restorations",
        ],
    },
    "Braces & Clear Aligners": {
        "badge": "DIGITAL ORTHODONTIC CORRECTION",
        "full_description": "Straighten your teeth and improve your bite with our advanced orthodontic treatment options. We provide custom invisible clear aligners that can be removed for eating and brushing, as well as discreet tooth-colored ceramic brackets. Every smile design journey starts with a 3D digital intraoral scan that projects your teeth's movement week by week until reaching your ideal smile.",
        "highlights": [
            "Zero-impression 3D digital intraoral scanning with instant simulation",
            "Removable, custom-molded invisible clear aligners for maximum convenience",
            "Low-profile aesthetic ceramic and self-ligating bracket options",
            "Correction of crowding, gaps, overlapping teeth, overbites, and crossbites",
            "Custom post-treatment retainers to ensure your results last a lifetime",
        ],
    },
    "Cosmetic Dentistry": {
        "badge": "CUSTOM SMILE MAKEOVERS",
        "full_description": "Cosmetic dentistry harmonizes science and artistic vision to create balanced, dazzling smiles. Whether you wish to repair minor chips with direct composite bonding, close gaps with ultra-thin porcelain veneers, or reshape an uneven gumline, our cosmetic clinicians craft each detail to complement your unique facial features, lip dynamics, and complexion.",
        "highlights": [
            "Digital Smile Design (DSD) preview before any treatment begins",
            "Ultra-thin handcrafted porcelain veneers with lifelike light translucency",
            "Minimally invasive composite resin bonding for chipped or uneven edges",
            "Gentle aesthetic gum recontouring for balanced tooth-to-gum proportions",
            "Full smile transformations tailored for natural, long-lasting beauty",
        ],
    },
    "Children's Dentistry": {
        "badge": "GENTLE PEDIATRIC CARE",
        "full_description": "Creating a positive, trusting relationship with dental care during childhood sets the stage for a lifetime of healthy smiles. Our pediatric approach is tailored to make young patients feel secure and cheerful. From gentle cleanings and cavity-fighting mineral treatments to protective fissure sealants, we safeguard developing teeth while making every visit fun and relaxing.",
        "highlights": [
            "Warm, engaging environment designed to eliminate pediatric dental apprehension",
            "Gentle check-ups, tooth growth monitoring, and early bite tracking",
            "Cavity-preventing fluoride varnish and protective tooth sealants",
            "Gentle pediatric restorations with child-friendly terminology",
            "Interactive tooth-brushing instruction and nutritional guidance for parents",
        ],
    },
}

# --------------------------------------------------------------------------- #
# Branches, clinic tour, videos and awards
# --------------------------------------------------------------------------- #

BRANCHES = [
    {
        "name": "St. Thomas Mount Branch",
        "phone_display": "044-2234 5000",
        "phone_dial": "04422345000",
        "address": "5/66-1A, Butt Rd, St. Thomas Mount, Chennai - 600016",
        "map_embed_url": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3887.987843210000!2d80.17000000000000!3d13.01000000000000!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3a52674853a74b83%3A0x2181e234367e053f!2sMount%20Multispeciality%20Dental%20Clinic!5e0!3m2!1sen!2sin!4v1600000000000",
        "map_directions_url": "https://www.google.com/maps/place/Mount+Multispeciality+Dental+Clinic+St.Thomas+Mount,+Mount+Multispeciality+Dental+Clinic,+5%2F66-1A,+Butt+Rd,+Ramapuram,+Parangi+Malai,+St.Thomas+Mount,+Chennai,+Tamil+Nadu+600016/data=!4m2!3m1!1s0x3a52674853a74b83:0x2181e234367e053f!18m1!1e1",
        "is_primary": True,
        "sort_order": 0,
    },
    {
        "name": "Nungambakkam Branch",
        "phone_display": "044-2827 5000",
        "phone_dial": "04428275000",
        "address": "37/2, Jambulingam St, Nungambakkam, Chennai - 600034",
        "map_embed_url": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3886.000000000000!2d80.24000000000000!3d13.06000000000000!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3a526667f0d45565%3A0xcc5423acd0f5aee9!2sMount%20Multispeciality%20Dental%20Clinic%20Nungambakkam!5e0!3m2!1sen!2sin!4v1600000000001",
        "map_directions_url": "https://www.google.com/maps/place/Mount+Multispeciality+Dental+Clinic+Nungambakkam,+37%2F2,+Jambulingam+street,+Facing,+Valluvar+Kottam+High+Rd,+Nungambakkam,+Chennai,+Tamil+Nadu+600034/data=!4m2!3m1!1s0x3a526667f0d45565:0xcc5423acd0f5aee9!18m1!1e1",
        "is_primary": False,
        "sort_order": 1,
    },
]

CLINIC_IMAGES = [
    ("Modern Operatory Suites", "Designed for sterile comfort and advanced patient care", "hero-banners/dental-clinic.jpg"),
    ("High-Tech Treatment Stations", "Ergonomic dental units with integrated digital controls", "hero-banners/clinic-equipment.jpeg"),
    ("3D CBCT Diagnostic Scanning", "Ultra-low dose volumetric imaging for precision planning", "hero-banners/cbct-scan.jpeg"),
    ("Clinical Excellence & Sterilization", "Hospital-grade multi-stage autoclave hygiene standards", "site/why-dental.jpg"),
    ("Digital Intraoral Imaging", "High-magnification intraoral cameras for accurate assessment", "site/why-technology.jpg"),
    ("Inside Our Clinic", "A comfortable, modern space designed around patients", "clinic/sample-3.jpg"),
    ("Patient Care Suite", "Precision treatment delivered with a gentle touch", "clinic/sample-4.jpg"),
]

# Photos picked up from the project's ``sample/`` folder and shown in the clinic
# tour carousel. Update the files in ``sample/`` and re-run ``seed_demo`` (or
# ``update_doctor_images``) to publish new versions.
CLINIC_SAMPLE_IMAGES = {
    "3.jpg": ("clinic", "sample-3.jpg"),
    "4.jpg": ("clinic", "sample-4.jpg"),
}

YOUTUBE_VIDEOS = [
    ("Mount Dental Care - Clinic Tour", "https://www.youtube.com/embed/65tuw4Y7RU0"),
    ("Mount Dental Care - Patient Experience", "https://www.youtube.com/embed/GLrd0jHBkc0"),
]

AWARDS = [
    {
        "title": "Best Paper Presentation Award",
        "category": "Forensic Odontology",
        "description": "Dr. S. Natesh received the Best paper presentation award in Forensic Odontology from Padma Bhushan Brig. Anil Kohli, President, Dental Council of India on 20th January 2008 held in Dr. M.G.R. University, Chennai.",
        "venue": "Dr. M.G.R. University, Chennai",
        "event_date": "20th January 2008",
        "image": "awards/award_mgr_university.jpg",
        "sort_order": 0,
    },
    {
        "title": "Best Paper Presentation Award",
        "category": "Innovative Teaching Methods",
        "description": 'Dr. S. Natesh won the Best paper presentation Award on "FORMATIVE ASSESSMENT OF INNOVATIVE TEACHING METHODS" in APTCON08 on 13th July 08 held in Sri Ramachandra University, Chennai.',
        "venue": "Sri Ramachandra University, Chennai",
        "event_date": "13th July 2008",
        "image": "awards/award_srmc_university.jpg",
        "sort_order": 1,
    },
]

# --------------------------------------------------------------------------- #
# Editable text blocks
# --------------------------------------------------------------------------- #

# Every remaining hard-coded string in the React bundle is seeded here once as
# its own row. ``key`` is what the frontend reads; ``label`` explains it in Admin.
SITE_TEXTS = [
    # Header / hero ------------------------------------------------ #
    ("hero.metric_1_label", "Hero metric 1 label", "hero", "Experienced Dentists"),
    ("hero.metric_2_label", "Hero metric 2 label", "hero", "Advanced Equipment"),
    ("hero.metric_3_label", "Hero metric 3 label", "hero", "Affordable Care Plans"),
    ("hero.metric_4_label", "Hero metric 4 label", "hero", "Happy Patients Served"),
    ("hero.book_button", "Hero – Book Appointment button", "hero", "Book Appointment"),
    ("hero.call_button", "Hero – Call Now button", "hero", "Call Now"),
    ("header.book_button", "Header – Book Appointment button", "header", "Book Appointment"),

    # Offer --------------------------------------------------------- #
    ("offer.button_text", "Offer banner button", "offer", "Book Today"),

    # Services ------------------------------------------------------ #
    ("services.heading.eyebrow", "Services heading eyebrow", "services", "WORLD-CLASS DENTAL CARE"),
    ("services.heading.title", "Services heading title", "services", "Comprehensive Dental Services for Every Age"),
    ("services.heading.text", "Services heading description", "services", "From preventative hygiene to intricate smile makeovers, our clinic utilizes state-of-the-art dental technology to ensure painless, lasting outcomes."),
    ("services.learn_more", "Service card link", "services", "Learn More"),
    ("services.cta.question", "Services CTA question", "services", "Not sure which treatment suits your smile best?"),
    ("services.cta.button", "Services CTA button", "services", "Schedule a 15-Minute Diagnostic Consultation"),
    ("services.modal.highlights_title", "Popup highlights heading", "services", "Treatment Highlights & What's Included"),
    ("services.modal.book_button", "Popup book button", "services", "Book Appointment For This Service"),
    ("services.modal.close_button", "Popup close button", "services", "Close"),

    # About / mission ---------------------------------------------- #
    ("about.mission.title", "Mission card title", "about", "Our Mission"),
    ("about.mission.text", "Mission card text", "about", "To deliver exceptional, transparent, and comfortable, gentle dental healthcare that preserves natural smiles and uplifts self-esteem."),
    ("about.vision.title", "Vision card title", "about", "Our Vision"),
    ("about.vision.text", "Vision card text", "about", "To become the community's lifelong oral health home, renowned for clinical precision, integrity, and warmth."),

    # Experts ------------------------------------------------------- #
    ("experts.founder_tag", "Lead doctor badge", "experts", "Lead Dentist & Founder"),
    ("experts.education_label", "Credential – Education label", "experts", "Education & Credentials"),
    ("experts.tenure_label", "Credential – Tenure label", "experts", "Clinical Tenure"),
    ("experts.expertise_label", "Credential – Expertise label", "experts", "Core Expertise"),
    ("experts.membership_label", "Credential – Membership label", "experts", "Indian Membership"),
    ("experts.book_button", "Book with doctor button", "experts", "Book with"),
    ("experts.next_available", "Next available note", "experts", "Next Available: Today at 3:30 PM"),

    # Awards -------------------------------------------------------- #
    ("awards.heading.eyebrow", "Awards heading eyebrow", "awards", "ACADEMIC HONORS & RECOGNITIONS"),
    ("awards.heading.title", "Awards heading title", "awards", "Awards & Scientific Achievements"),
    ("awards.heading.text", "Awards heading description", "awards", "Honoring Dr. S. Natesh's distinguished research contributions, forensic odontology achievements, and leadership in dental clinical education."),

    # Appointment --------------------------------------------------- #
    ("appointment.form_title", "Booking form title", "appointment", "Book Your Appointment"),
    ("appointment.form_subtitle", "Booking form subtitle", "appointment", "Fill in the details below to request a convenient time slot."),
    ("appointment.bullet_1", "Booking benefit 1", "appointment", "Personalized initial consultation for new patients"),
    ("appointment.bullet_2", "Booking benefit 2", "appointment", "Instant Email verification & calendar confirmation"),
    ("appointment.bullet_3", "Booking benefit 3", "appointment", "Prefer calling? Our reception team is happy to help you book a convenient slot."),
    ("appointment.field.name.label", "Form label – name", "appointment", "FULL NAME *"),
    ("appointment.field.name.placeholder", "Form placeholder – name", "appointment", "John Doe"),
    ("appointment.field.mobile.label", "Form label – mobile", "appointment", "MOBILE NUMBER *"),
    ("appointment.field.mobile.placeholder", "Form placeholder – mobile", "appointment", "+91 98765 43210"),
    ("appointment.field.email.label", "Form label – email", "appointment", "EMAIL ADDRESS *"),
    ("appointment.field.email.placeholder", "Form placeholder – email", "appointment", "john@example.com"),
    ("appointment.field.date.label", "Form label – date", "appointment", "PREFERRED DATE *"),
    ("appointment.field.date.placeholder", "Form placeholder – date", "appointment", "dd/mm/yyyy"),
    ("appointment.field.message.label", "Form label – message", "appointment", "ADDITIONAL MESSAGE OR SYMPTOMS"),
    ("appointment.field.message.placeholder", "Form placeholder – message", "appointment", "Tell us if you have toothache, sensitivity, or specific goals..."),
    ("appointment.field.treatment.label", "Form label – treatment", "appointment", "TREATMENT TYPE *"),
    ("appointment.field.treatment.placeholder", "Form dropdown placeholder", "appointment", "Select Dental Service"),
    ("appointment.submit", "Booking submit button", "appointment", "Confirm & Book Appointment"),
    ("appointment.privacy", "Booking privacy note", "appointment", "Your information is securely verified by email before the appointment is created."),
    ("appointment.otp.step", "OTP popup – step label", "appointment", "STEP 1 OF 2 • INSTANT EMAIL VERIFICATION"),
    ("appointment.otp.title", "OTP popup – title", "appointment", "Verify Your Email Address"),
    ("appointment.otp.subtitle", "OTP popup – subtitle (email appended)", "appointment", "Enter the 4-digit verification code sent by Gmail to"),
    ("appointment.otp.summary", "OTP popup – summary label", "appointment", "Appointment • Preferred Date:"),
    ("appointment.otp.edit", "OTP popup – edit button", "appointment", "Edit / Change"),
    ("appointment.otp.code_label", "OTP popup – code label", "appointment", "ENTER 4-DIGIT CODE"),
    ("appointment.otp.valid_for", "OTP popup – validity label", "appointment", "Code valid for"),
    ("appointment.otp.expired", "OTP popup – expired note", "appointment", "This code has expired — request a new one."),
    ("appointment.otp.resend_question", "OTP popup – resend question", "appointment", "Didn't receive the code?"),
    ("appointment.otp.resend_in", "OTP popup – resend countdown label", "appointment", "Resend in"),
    ("appointment.otp.resend_ready", "OTP popup – resend ready note", "appointment", "You can resend now"),
    ("appointment.otp.resend_button", "OTP popup – resend button", "appointment", "Resend code"),
    ("appointment.otp.resend_sending", "OTP popup – resend busy label", "appointment", "Sending..."),
    ("appointment.otp.sent_note", "OTP popup – delivery note", "appointment", "One email with your code was sent — check your Gmail inbox and spam folder."),
    ("appointment.otp.demo_prefix", "OTP popup – demo code prefix", "appointment", "Demo code:"),
    ("appointment.otp.submit", "OTP popup – confirm button", "appointment", "Verify & Submit Appointment"),
    ("appointment.otp.verifying", "OTP popup – verifying label", "appointment", "Verifying..."),
    ("appointment.otp.secure", "OTP popup – security note", "appointment", "Secure email verification • Your information is protected"),
    ("appointment.success.title", "Thanks popup – title", "appointment", "Appointment Request Received!"),
    ("appointment.success.text", "Thanks popup – message", "appointment", "Our patient care team will contact you shortly to confirm."),

    # Contact ------------------------------------------------------- #
    ("contact.call_label", "Contact – call label", "contact", "CALL DIRECTLY"),
    ("contact.email_label", "Contact – email label", "contact", "EMAIL SUPPORT"),
    ("contact.locations_label", "Contact – locations label", "contact", "CLINIC LOCATIONS"),
    ("contact.directions", "Get directions link", "contact", "Get Directions"),
    ("contact.hero_note", "Contact sidebar note", "contact", "Our care coordinators reply within 15 minutes during clinic hours."),

    # Phone chooser modal ------------------------------------------- #
    ("phone_modal.title", "Phone chooser title", "header", "Call Mount Dental Care"),
    ("phone_modal.description", "Phone chooser description", "header", "Select a branch below to connect directly with our reception team:"),

    # Footer -------------------------------------------------------- #
    ("footer.quick_links_title", "Footer – quick links heading", "footer", "QUICK LINKS"),
    ("footer.treatments_title", "Footer – treatments heading", "footer", "KEY TREATMENTS"),
    ("footer.hours_title", "Footer – hours heading", "footer", "CLINIC HOURS"),
]


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def _is_empty(value):
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    name = getattr(value, "name", None)  # FileField / ImageField
    if name is not None:
        return not name
    return False


def doctor_image_filenames():
    """File names of the doctor photos referenced by the seed data."""
    return {spec["image"].rsplit("/", 1)[-1] for spec in DOCTORS}


def sample_media_targets():
    """``sample/<name>`` -> ``(seed_media sub-folder, stored file name)``."""
    targets = {name: ("doctors", name) for name in doctor_image_filenames()}
    targets.update(CLINIC_SAMPLE_IMAGES)
    return targets


def sync_sample_media():
    """Refresh bundled photos from the project's ``sample/`` folder.

    Covers the doctor portraits and the clinic tour photos the seed data knows
    about. Only files whose name is already expected are copied, so an unrelated
    image dropped in ``sample/`` can never leak into the bundle.
    Returns the file names that actually changed.
    """
    refreshed = []
    if not SAMPLE_MEDIA_DIR.is_dir():
        return refreshed

    targets = sample_media_targets()
    for source in sorted(SAMPLE_MEDIA_DIR.iterdir()):
        spec = targets.get(source.name)
        if not source.is_file() or not spec:
            continue
        folder, filename = spec
        target = SEED_MEDIA_DIR / folder / filename
        if target.is_file() and target.read_bytes() == source.read_bytes():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        refreshed.append(source.name)
    return refreshed


def install_media(force=False):
    """Copy ``seed_media/**`` into ``MEDIA_ROOT``.

    Returns a ``(copied, kept)`` tuple. Existing files are kept unless *force*
    is set, so Admin uploads are never replaced by the bundled samples.
    """
    copied = kept = 0
    if not SEED_MEDIA_DIR.exists():
        return copied, kept
    media_root = Path(settings.MEDIA_ROOT)
    for source in sorted(SEED_MEDIA_DIR.rglob("*")):
        if not source.is_file():
            continue
        target = media_root / source.relative_to(SEED_MEDIA_DIR)
        if target.exists() and not force:
            kept += 1
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        # copy2 preserves the source mtime, and the API builds its image URLs as
        # ``?v=<mtime>``. Stamping the publish time guarantees that token changes
        # whenever a file is installed, so browsers cannot keep an older photo.
        os.utime(target, None)
        copied += 1
    return copied, kept


def _upsert(model, lookup, defaults, reset=False):
    """Create the row when missing, then fill blank fields (everything on reset).

    Returns ``(object, action)`` where action is ``created``/``updated``/``kept``.
    """
    obj = model.objects.filter(**lookup).first()
    if obj is None:
        return model.objects.create(**{**lookup, **defaults}), "created"
    fields = []
    for field, value in defaults.items():
        current = getattr(obj, field)
        if not (reset or _is_empty(current)):
            continue
        if not reset and _is_empty(value):
            continue
        setattr(obj, field, value)
        fields.append(field)
    if fields:
        obj.save(update_fields=fields)
        return obj, "updated"
    return obj, "kept"


def seed_content(reset=False):
    """Apply every default record and return ``(counts, log_lines)``."""
    counts = {"created": 0, "updated": 0, "kept": 0}
    log = []

    def apply(model, label, lookup, defaults):
        obj, action = _upsert(model, lookup, defaults, reset)
        counts[action] += 1
        log.append(f"{label}: {action}")
        return obj

    # Site settings ------------------------------------------------ #
    apply(SiteSettings, "Site settings", {"pk": 1}, SITE_FIELDS)

    # Navigation ---------------------------------------------------- #
    # Keyed by label: the section each link opens is derived from the label, so
    # there is no anchor to keep in sync.
    for item in NAV_ITEMS:
        apply(NavItem, f'Nav "{item["label"]}"', {"label": item["label"]},
              {"sort_order": item["sort_order"], "active": True})

    apply(OfferBanner, "Offer banner", {"pk": 1}, {**OFFER, "active": True})

    # Services / trust ---------------------------------------------- #
    for icon, title, description in SERVICES:
        details = SERVICE_DETAILS.get(title, {})
        apply(Service, f'Service "{title}"', {"title": title},
              {"icon": icon, "description": description,
               "badge": details.get("badge", ""),
               "full_description": details.get("full_description", ""),
               "highlights": "\n".join(details.get("highlights", [])),
               "sort_order": [s[1] for s in SERVICES].index(title),
               "active": True})

    for icon, title, description in TRUST_FEATURES:
        apply(TrustFeature, f'Trust "{title}"', {"title": title},
              {"icon": icon, "description": description,
               "sort_order": [t[1] for t in TRUST_FEATURES].index(title),
               "active": True})

    # Doctors ------------------------------------------------------- #
    for doctor in DOCTORS:
        apply(Doctor, f'Doctor "{doctor["name"]}"', {"name": doctor["name"]},
              {**{k: v for k, v in doctor.items() if k != "name"}, "active": True})

    # Gallery ------------------------------------------------------- #
    for item in GALLERY:
        apply(GalleryItem, f"Gallery #{item['sort_order'] + 1}", {"sort_order": item["sort_order"]},
              {**{k: v for k, v in item.items() if k != "sort_order"}, "active": True})

    # Addresses / hours --------------------------------------------- #
    for index, address in enumerate(ADDRESSES):
        apply(ClinicAddress, f"Address #{index + 1}", {"address": address},
              {"label": "Clinic Location", "sort_order": index, "active": True})

    for index, (day, hours, emergency) in enumerate(HOURS):
        apply(ClinicHour, f'Hours "{day}"', {"day": day},
              {"hours": hours, "emergency": emergency, "sort_order": index})

    # Footer links -------------------------------------------------- #
    for group, label, url in FOOTER_LINKS:
        same_group = [f for f in FOOTER_LINKS if f[0] == group]
        apply(FooterLink, f'Footer "{label}"', {"group": group, "label": label},
              {"url": url, "sort_order": same_group.index((group, label, url)), "active": True})

    # Editable page copy -------------------------------------------- #
    for key, eyebrow, title, description in PAGES:
        apply(PageContent, f'Page "{key}"', {"key": key},
              {"eyebrow": eyebrow, "title": title, "description": description, "active": True})

    # Hero carousel -------------------------------------------------- #
    # Older seed versions created untitled banners (and pointed some at gallery
    # photos). Drop those leftovers so the carousel matches the seeded slides.
    stale = HeroBanner.objects.filter(title="").delete()[0]
    if stale:
        log.append(f"Removed {stale} untitled hero banner(s)")

    for title, media_type, media, order in HERO_BANNERS:
        apply(HeroBanner, f'Hero banner "{title}"', {"title": title},
              {"media_type": media_type, "media": media, "sort_order": order, "active": True})

    # Email templates ----------------------------------------------- #
    for template_type, subject, body in EMAIL_TEMPLATES:
        apply(EmailTemplate, f'Email template "{template_type}"', {"template_type": template_type},
              {"subject": subject, "body": body, "active": True})

    # Editable text blocks ------------------------------------------ #
    for index, (key, label, group, value) in enumerate(SITE_TEXTS):
        apply(SiteText, f'Text "{key}"', {"key": key},
              {"label": label, "group": group, "value": value, "sort_order": index})

    # Branches ------------------------------------------------------ #
    for branch in BRANCHES:
        apply(Branch, f'Branch "{branch["name"]}"', {"name": branch["name"]},
              {**{k: v for k, v in branch.items() if k != "name"}, "active": True})

    # Clinic tour carousel ------------------------------------------ #
    for index, (title, caption, image) in enumerate(CLINIC_IMAGES):
        apply(ClinicImage, f"Clinic image #{index + 1}", {"title": title},
              {"caption": caption, "image": image, "sort_order": index, "active": True})

    # YouTube videos ------------------------------------------------ #
    for index, (title, url) in enumerate(YOUTUBE_VIDEOS):
        apply(YoutubeVideo, f'Video "{title}"', {"title": title},
              {"url": url, "sort_order": index, "active": True})

    # Awards -------------------------------------------------------- #
    for award in AWARDS:
        apply(Award, f'Award "{award["category"] or award["title"]}"',
              {"title": award["title"], "category": award["category"]},
              {**{k: v for k, v in award.items() if k not in ("title", "category")}, "active": True})

    return counts, log


def banner_titles():
    """Titles of the default hero banners (used by ``seed_hero_banners``)."""
    return sorted(BANNER_TITLES)
