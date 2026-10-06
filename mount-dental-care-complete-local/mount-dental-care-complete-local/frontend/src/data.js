export const site = {
  clinic: "Mount Dental Care",
  email: "mountdentalcare@gmail.com",
  hours: [],
  footer: [],
  addresses: [
    "5/66–1A, Butt road, St.Thomas Mount, Chennai 600016",
    "37/2, 1st Floor, Valluvar Kottam High Road, Nungambakkam, Chennai 600034"
  ],
  // CMS text blocks fetched from Django Admin (CMS -> Text blocks). The React
  // bundle keeps an inline fallback for every key, so a blank row (or a backend
  // that is briefly unreachable) never leaves a section without its copy.
  texts: {},
  topbarHours: "Mon-Sat : Morning - 10.00 AM - 01.00 PM | Evening 05.00 PM - 08.30 PM",
  whatsappNumber: "917010823417",
  footerAbout: "",
  footerCopyright: ""
};

// Navigation is managed in Django Admin (CMS -> Nav Items). Each link scrolls
// to the page section whose id matches the label, e.g. "Awards" -> #awards.
export const nav = [
  { label: "Home" },
  { label: "Why Choose Us" },
  { label: "Our Dentists" },
  { label: "About Clinic" },
  { label: "Smile Gallery" },
  { label: "Awards" }
];

// Hero banners are fetched dynamically from Django Backend (CMS -> Hero Banners).
export const heroBanners = [];

// Clinic branches (CMS -> Branches). Drives the top bar, call chooser, contact
// cards and the map. The bundled defaults keep the contact details visible
// before the first API response.
export const branches = [
  {
    name: "St. Thomas Mount Branch",
    phone_display: "044-2234 5000",
    phone_dial: "04422345000",
    address: "5/66-1A, Butt Rd, St. Thomas Mount, Chennai - 600016",
    is_primary: true
  },
  {
    name: "Nungambakkam Branch",
    phone_display: "044-2827 5000",
    phone_dial: "04428275000",
    address: "37/2, Jambulingam St, Nungambakkam, Chennai - 600034",
    is_primary: false
  }
];

// Clinic tour carousel (CMS -> Clinic tour images).
export const clinicImages = [
  { id: "clinic-1", src: "/media/hero-banners/dental-clinic.jpg", title: "Modern Operatory Suites", caption: "Designed for sterile comfort and advanced patient care" },
  { id: "clinic-2", src: "/media/hero-banners/clinic-equipment.jpeg", title: "High-Tech Treatment Stations", caption: "Ergonomic dental units with integrated digital controls" },
  { id: "clinic-3", src: "/media/hero-banners/cbct-scan.jpeg", title: "3D CBCT Diagnostic Scanning", caption: "Ultra-low dose volumetric imaging for precision planning" },
  { id: "clinic-4", src: "/media/site/why-dental.jpg", title: "Clinical Excellence & Sterilization", caption: "Hospital-grade multi-stage autoclave hygiene standards" },
  { id: "clinic-5", src: "/media/site/why-technology.jpg", title: "Digital Intraoral Imaging", caption: "High-magnification intraoral cameras for accurate assessment" }
];

// Embedded tour videos (CMS -> YouTube videos).
export const youtubeVideos = [
  { id: "yt-1", title: "Mount Dental Care - Clinic Tour", url: "https://www.youtube.com/embed/65tuw4Y7RU0" },
  { id: "yt-2", title: "Mount Dental Care - Patient Experience", url: "https://www.youtube.com/embed/GLrd0jHBkc0" }
];

// Academic honours (CMS -> Awards).
export const awards = [
  {
    id: "award-1",
    image: "/awards/award_mgr_university.jpg",
    title: "Best Paper Presentation Award",
    category: "Forensic Odontology",
    event_date: "20th January 2008",
    venue: "Dr. M.G.R. University, Chennai",
    description: "Dr. S. Natesh received the Best paper presentation award in Forensic Odontology from Padma Bhushan Brig. Anil Kohli, President, Dental Council of India on 20th January 2008 held in Dr. M.G.R. University, Chennai."
  },
  {
    id: "award-2",
    image: "/awards/award_srmc_university.jpg",
    title: "Best Paper Presentation Award",
    category: "Innovative Teaching Methods",
    event_date: "13th July 2008",
    venue: "Sri Ramachandra University, Chennai",
    description: 'Dr. S. Natesh won the Best paper presentation Award on "FORMATIVE ASSESSMENT OF INNOVATIVE TEACHING METHODS" in APTCON08 on 13th July 08 held in Sri Ramachandra University, Chennai.'
  }
];

export const services = [
  { icon: "stethoscope", title: "General Dentistry", text: "Comprehensive oral exams, digital X-rays, cavity diagnostics, and routine tooth health upkeep for the whole family." },
  { icon: "sparkles", title: "Teeth Cleaning & Polishing", text: "Gentle ultrasonic scaling to eliminate stubborn plaque, tartar buildup, and bad breath for fresh, clean gums." },
  { icon: "sun", title: "Teeth Whitening", text: "Advanced laser light whitening that lifts enamel shades up to 8 times brighter in a single comfortable 45-minute visit." },
  { icon: "activity", title: "Root Canal Treatment", text: "Microscope-assisted, 100% painless endodontic procedures designed to save natural teeth and relieve toothache immediately." },
  { icon: "shield", title: "Dental Implants", text: "Permanent, natural-feeling titanium and zirconia root replacements that look, bite, and last just like real teeth." },
  { icon: "layers", title: "Braces & Clear Aligners", text: "Custom invisible aligners and discreet ceramic brackets to align crowded teeth, correct bites, and enhance symmetry." },
  { icon: "smile", title: "Cosmetic Dentistry", text: "Custom porcelain veneers, aesthetic bonding, and gummy smile contouring for picture-perfect Hollywood smiles." },
  { icon: "baby", title: "Children's Dentistry", text: "Fun, gentle pediatric care, fluoride coatings, sealant applications, and dental habit coaching for cheerful kids." }
];

export const trustCards = [
  ["award", "Experienced Dental Specialists", "Endodontists, implantologists, and pediatric dental specialists with over 21+ years of combined mastery."],
  ["cpu", "Modern Technology", "Equipped with 3D CBCT scanners, intraoral digital cameras, and painless computer-guided laser dentistry."],
  ["feather", "Comfortable Procedures", "Gentle injection techniques, nitrous oxide sedation options, and calming noise-cancelling entertainment headsets."],
  ["sparkle", "Hygienic Environment", "Hospital-grade 5-stage autoclave sterilization protocols, HEPA-filtered operatory suites, and single-use kits."],
  ["clipboard", "Personalized Treatment Plans", "Transparent upfront cost estimates, no hidden fees, and custom pacing that matches your schedule and budget."],
  ["bell", "Priority Dental Support", "Round-the-clock telephone assistance, immediate relief appointments, and fast-track trauma care."]
];

export const doctors = [
  { image: null, name: "Dr. S. NATESH M.D.S.", role: "Consultant Dental Surgeon, Endodontist & Implantologist • 21+ Years Experience", is_lead: true },
  { image: null, name: "Dr. N. PADMINI M.D.S.", role: "Consultant Dental Surgeon & Orthodontist", is_lead: false }
];

export const gallery = [
  { image: null, title: "INTERVIEW", text: "Interview of Dr. S. Natesh on SUN NEWS Satellite Television for DOCTOR'S NEWS." },
  { image: null, title: "INTERVIEW", text: "Interview of Dr. A.S. Subhashini on Doctor Sun News programme." },
  { image: null, title: "INTERVIEW", text: "Interview of Dr. A.S. Subhashini on SUN NEWS Satellite Television." },
  { image: null, title: "INTERVIEW", text: "Interview of Dr. Natesh on Makkal TV in Maruthuva Neram." },
  { image: null, title: "INTERVIEW", text: "Interview of Dr. A.S. Subhashini on SUN NEWS Satellite Television." },
  { image: null, title: "SUN NEWS INTERVIEW", text: "Interview of Dr. A.S. Subhashini on SUN NEWS Satellite Television." }
];