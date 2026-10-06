import React, { useEffect, useRef, useState } from "react";
import { site, nav, services, trustCards, doctors, gallery, heroBanners, branches, clinicImages, youtubeVideos, awards } from "./data";
import { loadSite, requestAppointmentOtp, verifyAppointmentOtp, mediaUrl } from "./api";
import { Icon } from "./icons";

// Read an Admin-managed text block, falling back to the copy bundled with the
// React app. Blank rows fall through, so editing or clearing a block in Django
// Admin can never leave a section without its text.
function text(key, fallback) {
  const value = site.texts?.[key];
  return (typeof value === "string" && value.trim()) ? value : fallback;
}

// Split a CMS "one item per line" field into a clean list.
function lines(value) {
  return String(value || "").split(/\r?\n/).map(x => x.trim()).filter(Boolean);
}

// Keep the bundled value when the Admin value is blank.
function orKeep(next, current) {
  return (typeof next === "string" && next.trim()) ? next : current;
}

// "St. Thomas Mount Branch" + "044-2234 5000" -> "St. Thomas Mount - 044-2234 5000".
function branchLabel(branch) {
  if (!branch) return "";
  const name = String(branch.name || "").replace(/\s+Branch$/i, "").trim();
  return [name, branch.phone_display].filter(Boolean).join(" - ");
}

// The footer lists a branch with its phone number on the line below it, so the
// "St. Thomas Mount - 044-2234 5000" label is split apart again for display.
function splitBranchLabel(label) {
  const parts = String(label || "").split(" - ");
  const phone = parts.length > 1 ? parts.pop().trim() : "";
  return { name: parts.join(" - ").trim(), phone };
}

// All branch phone numbers on one line, used by the contact cards.
function branchPhoneText() {
  return branches.filter(b => b.phone_display).map(branchLabel).join(" | ");
}

// Turn a nav label into the page section it scrolls to, so no anchor has to be
// maintained in Admin: "Why Choose Us" -> "why-choose-us".
function slugifyAnchor(label) {
  return String(label || "").toLowerCase().trim().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
}

// The copyright line is managed in Admin, so a stale "© 2025" saved there would
// otherwise come back with every CMS refresh. The year it shows is always the
// current one, and the bundled copy is the fallback when Admin has none.
function copyrightLine() {
  const year = new Date().getFullYear();
  const saved = String(site.footerCopyright || "").trim();
  const line = saved || `© ${year} Mount Dental Care & Clinic. All rights reserved.`;
  return line.replace(/©\s*(19|20)\d{2}/, `© ${year}`);
}

function SmartImage({ src, alt, className = "", placeholder, style }) {
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    setHasError(false);
  }, [src]);

  if (!src || hasError) {
    return placeholder || null;
  }

  return (
    <img
      src={src}
      alt={alt}
      className={className}
      style={style}
      onError={() => {
        console.warn("SmartImage failed to load:", src);
        setHasError(true);
      }}
    />
  );
}

const Logo = ({ alt = "Mount Dental Care logo", className = "" }) => {
  return (
    <SmartImage
      src={site.logo || "/assets/images/logo.png"}
      alt={alt}
      className={className}
      placeholder={<div className="brand-fallback" style={{ display: "block" }}><span>Mount</span><small>Dental Care</small></div>}
    />
  );
};

function hydrateFromBackend(data) {
  if (!data) return;
  if (data.site) Object.assign(site, {
    clinic: data.site.clinic_name ?? site.clinic,
    email: data.site.email ?? site.email,
    logo: mediaUrl(data.site.logo),
    heroBackgroundImage: mediaUrl(data.site.hero_background_image),
    heroTitle: data.site.hero_title ?? null,
    heroDescription: data.site.hero_description ?? null,
    metricDentists: data.site.metric_dentists ?? null,
    metricEquipment: data.site.metric_equipment ?? null,
    metricEmi: data.site.metric_emi ?? null,
    metricPatients: data.site.metric_patients ?? null,
    topbarHours: orKeep(data.site.topbar_hours, site.topbarHours),
    whatsappNumber: orKeep(data.site.whatsapp_number, site.whatsappNumber),
    footerAbout: orKeep(data.site.footer_about, site.footerAbout),
    footerCopyright: orKeep(data.site.footer_copyright, site.footerCopyright),
  });
  if (Array.isArray(data.nav) && data.nav.length) { nav.splice(0, nav.length, ...data.nav.map(x=>({label:x.label}))); }
  if (Array.isArray(data.services)) { services.splice(0, services.length, ...data.services.map(x=>({icon:x.icon,title:x.title,text:x.description,id:x.id,badge:x.badge,full_description:x.full_description,highlights:x.highlights}))); }
  if (Array.isArray(data.trust)) { trustCards.splice(0, trustCards.length, ...data.trust.map(x=>[x.icon,x.title,x.description])); }
  if (Array.isArray(data.doctors)) { doctors.splice(0, doctors.length, ...data.doctors.map(x=>({id:x.id,image:mediaUrl(x.image),name:x.name,role:x.role,bio:x.bio,education:x.education,expertise:x.expertise,tenure:x.tenure,memberships:x.memberships,is_lead:x.is_lead}))); }
  if (Array.isArray(data.gallery)) { gallery.splice(0, gallery.length, ...data.gallery.map(x=>({id:x.id,image:mediaUrl(x.image),title:x.title,text:x.description,video:mediaUrl(x.video)}))); }
  if (Array.isArray(data.hours)) { site.hours = data.hours.map(x=>({day:x.day,hours:x.hours,emergency:x.emergency})); }
  if (Array.isArray(data.footer)) { site.footer = data.footer.map(x=>({group:x.group,label:x.label,url:x.url,sort_order:x.sort_order})); }
  if (Array.isArray(data.hero_banners) && data.hero_banners.length) {
    const backendBanners = data.hero_banners
      .map(x => ({
        id: x.id,
        type: String(x.media_type || "image").toLowerCase(),
        src: mediaUrl(x.media),
        title: x.title || ""
      }))
      .filter(x => x.src);
    // Never replace the working bundled carousel with empty/incomplete
    // admin records. If Admin has valid media, use it; otherwise keep
    // the bundled fallback banners.
    if (backendBanners.length) {
      heroBanners.splice(0, heroBanners.length, ...backendBanners);
    }
  }
  if (data.addresses?.length) site.addresses = data.addresses.map(x=>x.address);
  if (data.offer) site.offer=data.offer;
  if (data.pages?.length) site.pages=Object.fromEntries(data.pages.map(x=>[x.key,x]));
  // Text blocks: only non-blank values override the bundled copy.
  if (Array.isArray(data.texts)) {
    site.texts = Object.fromEntries(
      data.texts
        .filter(x => x && x.key && typeof x.value === "string" && x.value.trim())
        .map(x => [x.key, x.value])
    );
  }
  // Branches must always exist (they carry the phone contacts), so an empty
  // Admin list keeps the bundled defaults instead of blanking the top bar.
  if (Array.isArray(data.branches) && data.branches.length) {
    branches.splice(0, branches.length, ...data.branches.map(x=>({
      id:x.id, name:x.name, phone_display:x.phone_display, phone_dial:x.phone_dial,
      address:x.address, map_embed_url:x.map_embed_url, map_directions_url:x.map_directions_url,
      is_primary:x.is_primary
    })));
  }
  if (Array.isArray(data.clinic_images)) {
    clinicImages.splice(0, clinicImages.length, ...data.clinic_images
      .map(x=>({id:x.id, src:mediaUrl(x.image), title:x.title, caption:x.caption}))
      .filter(x=>x.src));
  }
  if (Array.isArray(data.youtube)) {
    youtubeVideos.splice(0, youtubeVideos.length, ...data.youtube
      .map(x=>({id:x.id, title:x.title, url:x.url}))
      .filter(x=>x.url));
  }
  if (Array.isArray(data.awards)) {
    awards.splice(0, awards.length, ...data.awards.map(x=>({
      id:x.id, image:mediaUrl(x.image), title:x.title, category:x.category,
      description:x.description, venue:x.venue, event_date:x.event_date
    })));
  }
}

function Header({ onBook, onCall }) {
  const [open, setOpen] = useState(false);
  // The bars are one sticky stack whose height depends on how long the
  // admin's phone numbers / hours turn out to be, so the anchor scroll
  // offset is measured rather than assumed. `--stack-h` feeds
  // `html { scroll-padding-top }` in styles.css.
  const stackRef = useRef(null);
  useEffect(() => {
    const el = stackRef.current;
    if (!el) return;
    const root = document.documentElement;
    const apply = () => root.style.setProperty("--stack-h", `${el.offsetHeight}px`);
    apply();
    if (typeof ResizeObserver === "undefined") return;
    const observer = new ResizeObserver(apply);
    observer.observe(el);
    return () => observer.disconnect();
  }, []);
  const clinicWords = String(site.clinic || "Mount Dental Care").trim().split(/\s+/);
  const clinicFirst = clinicWords[0] || "Mount";
  const clinicRest = clinicWords.slice(1).join(" ");
  const phoneBranches = branches.filter(b => b.phone_display);
  return <>
    {/* The top bar and the header share one sticky container. Because the
        header sits *after* the bar in normal flow instead of being pinned at a
        guessed offset, CMS content of any length can wrap inside either bar
        without ever hiding the page underneath. */}
    <div className="site-header" ref={stackRef}>
    <div className="emergency-bar">
      <div className="emergency-left topbar-left">
        {phoneBranches.map((b, i) => (
          <React.Fragment key={b.id || b.name || i}>
            {i > 0 && <span className="topbar-sep">|</span>}
            <a className="topbar-link" href={b.phone_dial ? `tel:${b.phone_dial}` : undefined}>
              <Icon name="phone" size={14} /> {branchLabel(b)}
            </a>
          </React.Fragment>
        ))}
      </div>
      <div className="emergency-right">
        <span className="topbar-hours">
          <Icon name="clock" size={14} /> {site.topbarHours}
        </span>
      </div>
    </div>
    <header className="header">
      <a className="brand" href="#home" aria-label={site.clinic || "Mount Dental Care"}>
        <Logo alt={`${site.clinic || "Mount Dental Care"} logo`} />
        <div className="brand-fallback"><span>{clinicFirst}</span>{clinicRest && <small>{clinicRest}</small>}</div>
      </a>
      <button className="mobile-menu" type="button" aria-label={open ? "Close navigation menu" : "Open navigation menu"} aria-expanded={open} aria-controls="primary-navigation" onClick={() => setOpen(v=>!v)}><Icon name={open ? "x" : "menu"}/></button>
      <nav id="primary-navigation" className={open ? "nav open" : "nav"} aria-label="Primary navigation">
        {nav.map((item) => <a key={item.label} href={`#${slugifyAnchor(item.label)}`} onClick={()=>setOpen(false)}>{item.label}</a>)}
        <button className="nav-book-btn primary small" onClick={()=>{setOpen(false); onBook?.()}}><Icon name="calendar" size={16}/> {text("header.book_button", "Book Appointment")}</button>
      </nav>
      <div className="header-actions">
        <button className="icon-btn" type="button" onClick={() => onCall?.()} aria-label="Call"><Icon name="phone" size={19}/></button>
        <button className="header-book-btn primary small" onClick={onBook}><Icon name="calendar" size={16}/> {text("header.book_button", "Book Appointment")}</button>
      </div>
    </header>
    </div>
  </>;
}

function PhoneSelectorModal({ onClose }) {
  const list = branches.filter(b => b.phone_display || b.phone_dial || b.name);

  return (
    <div className="phone-modal-backdrop" onMouseDown={e => e.target === e.currentTarget && onClose?.()}>
      <div className="phone-modal">
        <button className="phone-modal-close" onClick={onClose} aria-label="Close modal">
          <Icon name="x" size={18} />
        </button>
        <div className="phone-modal-header">
          <span><Icon name="phone" size={20} /></span>
          <h3>{text("phone_modal.title", `Call ${site.clinic || "Mount Dental Care"}`)}</h3>
        </div>
        <p className="phone-modal-desc">{text("phone_modal.description", "Select a branch below to connect directly with our reception team:")}</p>
        <div className="phone-modal-branches">
          {list.map((b, i) => {
            const dial = b.phone_dial || String(b.phone_display || "").replace(/[^0-9+]/g, "");
            return (
              <a key={b.id || b.name || i} href={dial ? `tel:${dial}` : undefined} className="phone-branch-btn">
                <div className="phone-branch-info">
                  <span className="phone-branch-name">{b.name}</span>
                  {b.phone_display && <span className="phone-branch-num">{b.phone_display}</span>}
                </div>
                <Icon name="phone" size={18} color="#078fd0" />
              </a>
            );
          })}
        </div>
      </div>
    </div>
  );
}

function Hero({ onBook, onCall }) {
  const [slide, setSlide] = useState(0);
  const slides = heroBanners.filter(x => x?.src);

  useEffect(() => {
    if (slide >= slides.length && slides.length) setSlide(0);
  }, [slides.length, slide]);

  useEffect(() => {
    if (slides.length < 2) return;
    // Hero banner carousel auto-plays every 5 seconds.
    const timer = setInterval(() => setSlide(v => (v + 1) % slides.length), 5000);
    return () => clearInterval(timer);
  }, [slides.length]);

  const active = slides[slide];
  const fallback = site.heroBackgroundImage;
  // Admin can use "|" in the Hero title to control the line breaks; otherwise
  // the words are split into up to three balanced lines. The heading is not
  // given a fixed height, so any wording still wraps without breaking layout.
  const heroLines = (() => {
    const title = String(site.heroTitle || "").trim();
    if (!title) return ["Healthy Smiles,", "Lifelong", "Confidence"];
    if (title.includes("|")) return title.split("|").map(x => x.trim()).filter(Boolean);
    const words = title.split(/\s+/).filter(Boolean);
    if (words.length <= 2) return [title];
    const size = Math.ceil(words.length / 3);
    return [words.slice(0, size), words.slice(size, size * 2), words.slice(size * 2)]
      .map(part => part.join(" ")).filter(Boolean);
  })();

  return <section id="home" className="hero">
    <div className="hero-bg" aria-hidden="true">
      {active?.type === "video" ? (
        <video key={active.src} className="hero-bg-media" src={active.src} autoPlay muted loop playsInline preload="auto" />
      ) : active?.src ? (
        <img key={active.src} className="hero-bg-media" src={active.src} alt="" />
      ) : fallback ? (
        <img className="hero-bg-media" src={fallback} alt="" />
      ) : null}
      <div className="hero-bg-overlay" />
    </div>
    <div className="hero-inner">
      <div className="hero-copy">
        <h1>{heroLines.map((line, i) => i === 0
          ? <React.Fragment key={i}>{line}</React.Fragment>
          : <React.Fragment key={i}><br/><span>{line}</span></React.Fragment>)}</h1>
        <p>{site.heroDescription || "Expert Dental Care with Advanced Technology and Personalized Treatment. Compassionate, gentle care designed for the whole family."}</p>
        <div className="hero-buttons"><button className="primary" onClick={onBook}><Icon name="calendar"/> {text("hero.book_button", "Book Appointment")}</button><button className="secondary" type="button" onClick={() => onCall?.()}><Icon name="phone"/> {text("hero.call_button", "Call Now")}</button></div>
      </div>
    </div>
    {slides.length > 1 && <div className="hero-carousel" aria-label="Hero banner carousel">
      <button type="button" className="hero-carousel-arrow" onClick={() => setSlide(v => (v - 1 + slides.length) % slides.length)} aria-label="Previous banner"><Icon name="chevronLeft" size={18} /></button>
      <div className="hero-carousel-dots">
        {slides.map((item, i) => <button key={item.id || item.src} type="button" className={i === slide ? "active" : ""} onClick={() => setSlide(i)} aria-label={`Show banner ${i + 1}`} aria-current={i === slide ? "true" : undefined} />)}
      </div>
      <button type="button" className="hero-carousel-arrow" onClick={() => setSlide(v => (v + 1) % slides.length)} aria-label="Next banner"><Icon name="chevronRight" size={18} /></button>
    </div>}
    <div className="hero-metrics">
      <Metric icon="user" number={site.metricDentists || "21+"} label={text("hero.metric_1_label", "Experienced Dentists")}/>
      <Metric icon="cpu" number={site.metricEquipment || "3D CBCT"} label={text("hero.metric_2_label", "Advanced Equipment")}/>
      <Metric icon="heart" number={site.metricEmi || "0% EMI"} label={text("hero.metric_3_label", "Affordable Care Plans")}/>
      <Metric icon="users" number={site.metricPatients || "5,000+"} label={text("hero.metric_4_label", "Happy Patients Served")}/>
    </div>
  </section>
}

function Metric({icon, number, label}) { return <div className="metric"><span><Icon name={icon} size={20}/></span><div><strong>{number}</strong><small>{label}</small></div></div> }

function FloatingActions({ onCall }) {
  return (
    <div className="floating-social" role="group" aria-label="Quick contact">
      
      {/* WhatsApp - connects to St. Thomas Mount reception */}
      <a
        className="wa"
        href={`https://wa.me/${site.whatsappNumber || "917010823417"}`}
        target="_blank"
        rel="noopener noreferrer"
        aria-label="Chat with Mount Dental Care on WhatsApp"
        title="Chat on WhatsApp"
      >
        <svg
          viewBox="0 0 32 32"
          width="28"
          height="28"
          aria-hidden="true"
          focusable="false"
        >
          <path
            fill="currentColor"
            d="M19.11 17.19c-.27-.14-1.6-.79-1.85-.88-.25-.09-.43-.14-.61.14-.18.27-.7.88-.86 1.06-.16.18-.32.2-.59.07-.27-.14-1.14-.42-2.17-1.34-.8-.71-1.34-1.58-1.5-1.85-.16-.27-.02-.42.12-.56.12-.12.27-.32.41-.48.14-.16.18-.27.27-.45.09-.18.05-.34-.02-.48-.07-.14-.61-1.47-.84-2.01-.22-.53-.45-.46-.61-.47h-.52c-.18 0-.48.07-.73.34-.25.27-.95.93-.95 2.26s.98 2.62 1.11 2.8c.14.18 1.92 2.93 4.65 4.11.65.28 1.16.45 1.56.57.66.21 1.26.18 1.73.11.53-.08 1.6-.65 1.82-1.28.23-.63.23-1.17.16-1.28-.07-.11-.25-.18-.52-.32z"
          />
          <path
            fill="currentColor"
            d="M16.03 3C8.85 3 3 8.79 3 15.91c0 2.27.6 4.48 1.74 6.42L3 29l6.82-1.78a13.02 13.02 0 0 0 6.21 1.58h.01c7.18 0 13.03-5.79 13.03-12.91C29.07 8.79 23.21 3 16.03 3zm0 23.58h-.01a10.86 10.86 0 0 1-5.53-1.5l-.4-.24-4.05 1.06 1.08-3.94-.26-.41a10.75 10.75 0 0 1-1.65-5.64c0-5.92 4.86-10.74 10.83-10.74 2.89 0 5.6 1.12 7.64 3.15a10.66 10.66 0 0 1 3.18 7.6c0 5.92-4.86 10.74-10.83 10.74z"
          />
        </svg>
      </a>

      {/* Call - opens branch chooser */}
      <button
        type="button"
        className="call"
        onClick={() => onCall?.()}
        aria-label="Call Mount Dental Care"
        title="Call Mount Dental Care"
      >
        <Icon name="phone" />
      </button>

      {/* Back to Top */}
      <button
        className="top"
        type="button"
        aria-label="Back to top"
        title="Back to top"
        onClick={() =>
          window.scrollTo({
            top: 0,
            behavior: "smooth",
          })
        }
      >
        <Icon name="arrowUp" size={20} />
      </button>
    </div>
  );
}


function Offer({ onBook }) {
  return (
    <section className="offer">
      <div>
        <span className="eyebrow dark">
          <Icon name="sparkles" size={13} style={{ marginRight: 5, verticalAlign: "middle" }} />
          {site.offer?.eyebrow || "ADVANCED DENTAL DIAGNOSTICS"}
        </span>

        <h2>
          {site.offer?.title || "3D CBCT Scan, Digital X-Ray & Intraoral Scan"}
        </h2>

        <p>
          {site.offer?.description ||
            "Get a complete picture of your oral health with our state-of-the-art diagnostic package. Our 3D CBCT Scan delivers high-precision volumetric imaging for implant planning and complex treatments, Digital X-Rays provide instant low-radiation tooth and bone assessment, and our Intraoral Camera Scan captures detailed images inside your mouth for accurate, painless diagnosis — all in one visit at Mount Dental Care, Chennai."}
        </p>
      </div>

      <button className="offer-btn" onClick={onBook}>
        {site.offer?.button_text || text("offer.button_text", "Book Today")}
        <Icon name="chevron" size={18} />
      </button>
    </section>
  );
}





function SectionHeading({eyebrow, title, text, light=false}) { return <div className={"section-heading"+(light?" light":"")}><span className="eyebrow">{eyebrow}</span><h2>{title}</h2>{text && <p>{text}</p>}</div> }


const serviceDetails = {
  "General Dentistry": {
    badge: "PREVENTIVE & DIAGNOSTIC CARE",
    fullDescription: "General dentistry forms the foundation of lifelong oral wellness for every member of your family. Our comprehensive consultations combine gentle physical exams, high-resolution digital intraoral cameras, and low-radiation digital radiography to detect early signs of decay, gum inflammation, and enamel wear long before they develop into complex dental issues.",
    highlights: [
      "Digital oral health evaluation and computerized cavity detection",
      "Low-radiation digital radiography & intraoral photo documentation",
      "Biocompatible tooth-colored composite restorations (aesthetic fillings)",
      "Preventive fluoride enamel applications & diagnostic bite analysis",
      "Customized home oral hygiene roadmap and dietary guidance"
    ],
  },
  "Teeth Cleaning & Polishing": {
    badge: "HYGIENE & GUM WELLNESS",
    fullDescription: "Professional dental prophylaxis is essential for removing stubborn bacterial plaque and calcified tartar deposits that regular brushing cannot reach. Our clinicians utilize state-of-the-art ultrasonic scalers with fine micro-water sprays to gently dislodge calculus from tooth surfaces and below the gumline, followed by diamond-paste polishing that restores silky-smooth enamel luster.",
    highlights: [
      "Advanced gentle ultrasonic scaling to eliminate calculus and plaque",
      "Subgingival cleaning to prevent gingivitis and periodontal disease",
      "Enamel polishing with specialized prophy paste for stain removal",
      "Removal of stubborn coffee, tea, and food surface discolorations",
      "Antiseptic gum soothing treatment for refreshed, healthy gums"
    ],
  },
  "Teeth Whitening": {
    badge: "AESTHETIC ENAMEL BRIGHTENING",
    fullDescription: "Restore natural luminosity to your smile with our professional in-office laser teeth whitening system. Unlike abrasive over-the-counter kits, our clinical procedure uses a pH-balanced whitening formulation activated by targeted cool-light laser technology. This lifts deep enamel and dentin stains while strictly shielding your gums and maintaining tooth comfort.",
    highlights: [
      "Up to 6 to 8 shades lighter in a single, relaxed clinical session",
      "Protective light-cured gingival barrier to safeguard delicate gums",
      "Controlled cool LED laser activation for optimal oxidation and stain breakdown",
      "Specialized post-whitening potassium nitrate desensitizing treatment",
      "Long-lasting, radiant results with comprehensive aftercare instructions"
    ],
  },
  "Root Canal Treatment": {
    badge: "MICROSCOPE-ASSISTED ENDODONTICS",
    fullDescription: "When deep decay, cracks, or trauma reach the tooth's innermost nerve chamber, modern endodontic therapy saves the natural tooth and relieves acute discomfort. Utilizing high-magnification dental operating microscopes and computerized digital apex locators, our specialist cleans, disinfects, and hermetically seals the root canal anatomy with biocompatible gutta-percha, allowing you to chew with comfort and confidence.",
    highlights: [
      "Computer-guided local anesthesia for a genuinely comfortable experience",
      "Microscope-assisted precision visualization of micro-canal branches",
      "Flexible nickel-titanium rotary file instrumentation for thorough cleaning",
      "Biocompatible hermetic seal to prevent reinfection and promote healing",
      "Custom crown preparation to restore structural strength and natural aesthetics"
    ],
  },
  "Dental Implants": {
    badge: "PERMANENT TOOTH RESTORATION",
    fullDescription: "Dental implants represent the modern gold standard for replacing missing teeth. An implant consists of a medical-grade titanium or zirconia post that integrates directly with the alveolar bone, mimicking a natural tooth root. Topped with a custom handcrafted ceramic crown, implants prevent bone loss, restore 100% bite functionality, and blend seamlessly with your surrounding natural teeth.",
    highlights: [
      "3D CBCT volumetric bone scan and virtual computer-guided planning",
      "Biocompatible titanium or metal-free ceramic zirconia implant fixtures",
      "Preserves natural jawbone density and youthful facial contours",
      "No alteration or shaving down of adjacent healthy teeth required",
      "Versatile solutions from single tooth replacement to full-arch restorations"
    ],
  },
  "Braces & Clear Aligners": {
    badge: "DIGITAL ORTHODONTIC CORRECTION",
    fullDescription: "Straighten your teeth and improve your bite with our advanced orthodontic treatment options. We provide custom invisible clear aligners that can be removed for eating and brushing, as well as discreet tooth-colored ceramic brackets. Every smile design journey starts with a 3D digital intraoral scan that projects your teeth's movement week by week until reaching your ideal smile.",
    highlights: [
      "Zero-impression 3D digital intraoral scanning with instant simulation",
      "Removable, custom-molded invisible clear aligners for maximum convenience",
      "Low-profile aesthetic ceramic and self-ligating bracket options",
      "Correction of crowding, gaps, overlapping teeth, overbites, and crossbites",
      "Custom post-treatment retainers to ensure your results last a lifetime"
    ],
  },
  "Cosmetic Dentistry": {
    badge: "CUSTOM SMILE MAKEOVERS",
    fullDescription: "Cosmetic dentistry harmonizes science and artistic vision to create balanced, dazzling smiles. Whether you wish to repair minor chips with direct composite bonding, close gaps with ultra-thin porcelain veneers, or reshape an uneven gumline, our cosmetic clinicians craft each detail to complement your unique facial features, lip dynamics, and complexion.",
    highlights: [
      "Digital Smile Design (DSD) preview before any treatment begins",
      "Ultra-thin handcrafted porcelain veneers with lifelike light translucency",
      "Minimally invasive composite resin bonding for chipped or uneven edges",
      "Gentle aesthetic gum recontouring for balanced tooth-to-gum proportions",
      "Full smile transformations tailored for natural, long-lasting beauty"
    ],
  },
  "Children's Dentistry": {
    badge: "GENTLE PEDIATRIC CARE",
    fullDescription: "Creating a positive, trusting relationship with dental care during childhood sets the stage for a lifetime of healthy smiles. Our pediatric approach is tailored to make young patients feel secure and cheerful. From gentle cleanings and cavity-fighting mineral treatments to protective fissure sealants, we safeguard developing teeth while making every visit fun and relaxing.",
    highlights: [
      "Warm, engaging environment designed to eliminate pediatric dental apprehension",
      "Gentle check-ups, tooth growth monitoring, and early bite tracking",
      "Cavity-preventing fluoride varnish and protective tooth sealants",
      "Gentle pediatric restorations with child-friendly terminology",
      "Interactive tooth-brushing instruction and nutritional guidance for parents"
    ],
  }
};

function ServiceModal({ service, onClose, onBook }) {
  if (!service) return null;

  // Backend-managed services carry an id, and their popup fields are edited in
  // Admin. The bundled list (shown before the API responds) falls back to the
  // copy shipped in this file, so the popup is never empty either way.
  const bundled = service.id ? {} : (serviceDetails[service.title] || {});
  const adminHighlights = lines(service.highlights);
  const fallbackHighlights = [
    "Personalized assessment tailored to your oral health goals",
    "Modern digital diagnostics and gentle clinical protocols",
    "Experienced dental specialists dedicated to comfortable outcomes",
    "Transparent treatment plans with clear guidance at every step"
  ];
  const details = {
    badge: service.badge || bundled.badge || "SPECIALIZED DENTAL SERVICE",
    fullDescription: service.full_description || bundled.fullDescription || service.text || service.description || "Comprehensive clinical care utilizing modern dental technology.",
    highlights: adminHighlights.length ? adminHighlights : ((bundled.highlights || []).length ? bundled.highlights : fallbackHighlights)
  };

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handleKeyDown);
    document.body.style.overflow = "hidden";
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "";
    };
  }, [onClose]);

  return (
    <div className="service-modal-backdrop" onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <div className="service-modal" role="dialog" aria-modal="true" aria-labelledby="service-modal-title">
        <button className="service-modal-close" onClick={onClose} aria-label="Close modal">
          <Icon name="x" size={20} />
        </button>

        <div className="service-modal-header">
          <span className="service-modal-icon">
            <Icon name={service.icon || "sparkles"} size={26} />
          </span>
          <div className="service-modal-badge">{details.badge}</div>
          <h3 id="service-modal-title">{service.title}</h3>
        </div>

        <div className="service-modal-body">
          <p className="service-modal-desc">{details.fullDescription}</p>

          <div className="service-modal-section">
            <h4>{text("services.modal.highlights_title", "Treatment Highlights & What's Included")}</h4>
            <ul className="service-modal-list">
              {details.highlights.map((item, idx) => (
                <li key={idx}>
                  <span className="service-check-icon"><Icon name="check" size={15} /></span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>

        </div>

        <div className="service-modal-footer">
          <button className="primary service-modal-book-btn" onClick={() => onBook(service.title)}>
            <Icon name="calendar" size={16} /> {text("services.modal.book_button", "Book Appointment For This Service")}
          </button>
          <button className="secondary service-modal-close-btn" onClick={onClose}>
            {text("services.modal.close_button", "Close")}
          </button>
        </div>
      </div>
    </div>
  );
}

function Services({ onBook }) {
  const [activeService, setActiveService] = useState(null);

  return (
    <section id="services" className="section services-section">
      <SectionHeading
        eyebrow={text("services.heading.eyebrow", "WORLD-CLASS DENTAL CARE")}
        title={text("services.heading.title", "Comprehensive Dental Services for Every Age")}
        text={text("services.heading.text", "From preventative hygiene to intricate smile makeovers, our clinic utilizes state-of-the-art dental technology to ensure painless, lasting outcomes.")}
      />
      <div className="service-grid">
        {services.map((s, i) => (
          <article className="service-card" key={s.title}>
            <span className={`service-icon c${i}`}>
              <Icon name={s.icon} size={22} />
            </span>
            <h3>{s.title}</h3>
            <p>{s.text}</p>
            <button type="button" onClick={() => setActiveService(s)}>
              {text("services.learn_more", "Learn More")} <Icon name="chevron" size={15} />
            </button>
          </article>
        ))}
      </div>
      <div className="service-cta">
        <span>{text("services.cta.question", "Not sure which treatment suits your smile best?")}</span>
        <button className="primary" onClick={() => onBook()}>
          <Icon name="help" /> {text("services.cta.button", "Schedule a 15-Minute Diagnostic Consultation")}
        </button>
      </div>
      {activeService && (
        <ServiceModal
          service={activeService}
          onClose={() => setActiveService(null)}
          onBook={(t) => {
            setActiveService(null);
            onBook(t);
          }}
        />
      )}
    </section>
  );
}


function ClinicImageCarousel() {
  const [current, setCurrent] = useState(0);
  // Same ref-based hover-pause as the dentists carousel, so moving the pointer
  // over the tour images cannot reset the auto-play countdown.
  const pausedRef = useRef(false);

  useEffect(() => {
    if (clinicImages.length < 2) return;
    // Clinic tour carousel auto-plays every 5 seconds.
    const interval = setInterval(() => {
      if (pausedRef.current) return;
      setCurrent(prev => (prev + 1) % clinicImages.length);
    }, 5000);
    return () => clearInterval(interval);
  }, [clinicImages.length]);

  // Keep the active slide valid when Admin adds or removes an image.
  useEffect(() => {
    setCurrent(prev => (clinicImages.length ? prev % clinicImages.length : 0));
  }, [clinicImages.length]);

  if (!clinicImages.length) return null;

  return (
    <div
      className="clinic-carousel-wrap"
      onMouseEnter={() => { pausedRef.current = true; }}
      onMouseLeave={() => { pausedRef.current = false; }}
      aria-label="Clinic Tour Carousel"
    >
      <div className="clinic-carousel-track">
        {clinicImages.map((img, idx) => (
          <div
            key={img.id || img.src}
            className={`clinic-carousel-slide ${idx === current ? "active" : ""}`}
            aria-hidden={idx !== current}
          >
            <img src={img.src} alt={img.title} loading="lazy" />
            <div className="clinic-carousel-overlay">
              <b>{img.title}</b>
              <small>{img.caption}</small>
            </div>
          </div>
        ))}
      </div>

      <button
        type="button"
        className="clinic-carousel-nav prev"
        onClick={() => setCurrent(prev => (prev - 1 + clinicImages.length) % clinicImages.length)}
        aria-label="Previous clinic image"
      >
        <Icon name="chevronLeft" size={20} />
      </button>
      <button
        type="button"
        className="clinic-carousel-nav next"
        onClick={() => setCurrent(prev => (prev + 1) % clinicImages.length)}
        aria-label="Next clinic image"
      >
        <Icon name="chevronRight" size={20} />
      </button>

      <div className="clinic-carousel-dots">
        {clinicImages.map((_, idx) => (
          <button
            key={idx}
            type="button"
            className={idx === current ? "active" : ""}
            onClick={() => setCurrent(idx)}
            aria-label={`Go to slide ${idx + 1}`}
          />
        ))}
      </div>
    </div>
  );
}

function WhyChoose() {
  return (
    <section id="why-choose-us" className="section why">
      <div className="why-left">
        <SectionHeading
          eyebrow={site.pages?.why?.eyebrow || "THE MOUNT DENTAL DIFFERENCE"}
          title={site.pages?.why?.title || "Why Patients Trust Mount Dental Care"}
          text={site.pages?.why?.description || "We believe visiting the dentist should be pleasant, relaxed, and genuinely reassuring. Our practice merges clinical excellence with heartfelt patient warmth."}
        />
        <ClinicImageCarousel />
        {youtubeVideos.length > 0 && (
          <div className="why-youtube-row">
            {youtubeVideos.map((video, i) => (
              <div className="why-youtube-frame" key={video.id || video.url || i}>
                <iframe
                  src={video.url}
                  title={video.title || `Clinic video ${i + 1}`}
                  frameBorder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                  referrerPolicy="strict-origin-when-cross-origin"
                  allowFullScreen
                />
              </div>
            ))}
          </div>
        )}
      </div>
      <div className="trust-grid">
        {trustCards.map(([icon, title, text]) => (
          <article className="trust-card" key={title}>
            <span><Icon name={icon} /></span>
            <h3>{title}</h3>
            <p>{text}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

// The clinic story is its own section now, placed above the doctor's section.
function About() {
  return (
    <section id="about-clinic" className="section about-full about-full-copy">
      <div className="about-copy-full">
        <SectionHeading
          eyebrow={site.pages?.about?.eyebrow || "ABOUT MOUNT DENTAL CARE"}
          title={site.pages?.about?.title || "Setting the Standard for Compassionate, Modern Dentistry"}
          text={site.pages?.about?.description || "Founded with a passion to redefine dental anxiety into a soothing, empowering health journey, Mount Dental Care has grown into one of the region's most reputable private practices. We combine world-class medical innovation with a boutique, patient-first touch."}
        />
        <div className="mission-grid">
          <article>
            <span><Icon name="target"/></span>
            <h3>{text("about.mission.title", "Our Mission")}</h3>
            <p>{text("about.mission.text", "To deliver exceptional, transparent, and comfortable, gentle dental healthcare that preserves natural smiles and uplifts self-esteem.")}</p>
          </article>
          <article>
            <span><Icon name="eye"/></span>
            <h3>{text("about.vision.title", "Our Vision")}</h3>
            <p>{text("about.vision.text", "To become the community's lifelong oral health home, renowned for clinical precision, integrity, and warmth.")}</p>
          </article>
        </div>
      </div>
    </section>
  );
}

function DoctorProfileCard({ doctor, reversed, onBook }) {
  if (!doctor) return null;
  const isLead = !!doctor.is_lead;
  const fallbackBio = isLead
    ? "Dr. S. Natesh is a Consultant Dental Surgeon, Endodontist and Implantologist with 21+ years of clinical experience. He has extensive experience in endodontic care, implantology, veneers and digital smile design, including more than 3,000 dental implant placements."
    : `${doctor.name || "Our specialist"} is part of the Mount Dental Care specialist team, delivering precise, comfortable and patient-first dental care with a focus on long-term oral health.`;
  return (
    <article className={"lead-doctor" + (reversed ? " lead-doctor-reverse" : "")}>
      <div className="lead-photo asset-box">
        <SmartImage src={doctor.image} alt={doctor.name || "Dentist"} placeholder={<div className="doctor-placeholder" style={{display:"flex"}}><Icon name="user" size={46}/><span>Upload doctor image in Admin</span></div>}/>
        {isLead && <span className="founder-tag"><Icon name="check"/> {text("experts.founder_tag", "Lead Dentist & Founder")}</span>}
      </div>
      <div className="lead-copy">
        <h3>{doctor.name || "Our Dentist"}</h3>
        <b className="role-blue">{doctor.role || "Consultant Dental Specialist"}</b>
        <p>{doctor.bio || fallbackBio}</p>
        <div className="credential-grid">
          <div><Icon name="award"/><b>{text("experts.education_label", "Education & Credentials")}</b><small>{doctor.education || "BDS, MDS"}</small></div>
          <div><Icon name="clock"/><b>{text("experts.tenure_label", "Clinical Tenure")}</b><small>{doctor.tenure || "Active Clinical Practice"}</small></div>
          <div><Icon name="check"/><b>{text("experts.expertise_label", "Core Expertise")}</b><small>{doctor.expertise || doctor.role || "General & Speciality Dentistry"}</small></div>
          <div><Icon name="shield"/><b>{text("experts.membership_label", "Indian Membership")}</b><small>{doctor.memberships || "Indian Dental Association (IDA)"}</small></div>
        </div>
        <div className="lead-action">
          <button className="primary" onClick={onBook}><Icon name="calendar"/>{text("experts.book_button", "Book with")} {doctor.name || "our team"}</button>
          <span>{text("experts.next_available", "Next Available: Today at 3:30 PM")}</span>
        </div>
      </div>
    </article>
  );
}

function Experts({onBook}) {
  const list = doctors.filter(Boolean);
  const [cur, setCur] = useState(0);
  const total = list.length;
  // Hover-pause lives in a ref, not state. Putting it in the effect deps meant
  // every mouseenter/mouseleave restarted the timer, so crossing the card kept
  // resetting the countdown and the carousel never looked like it auto-played.
  const pausedRef = useRef(false);

  useEffect(() => {
    if (total <= 1) return;
    // Auto-advance the Our Dentists carousel every 5 seconds.
    const t = setInterval(() => {
      if (pausedRef.current) return;
      setCur(p => (p + 1) % total);
    }, 5000);
    return () => clearInterval(t);
  }, [total]);

  useEffect(() => {
    if (cur >= total) setCur(0);
  }, [cur, total]);

  if (total === 0) return null;

  return (
    <section id="our-dentists" className="section experts">
      <SectionHeading eyebrow={site.pages?.experts?.eyebrow || "MEET OUR EXPERTS"} title={site.pages?.experts?.title || "Led by Renowned Dental Specialists"} text={site.pages?.experts?.description || "Our clinicians regularly train in Switzerland and the US in the latest micro-surgical and aesthetic protocols."}/>
      <div className="experts-carousel" onMouseEnter={() => { pausedRef.current = true; }} onMouseLeave={() => { pausedRef.current = false; }}>
        <div className="experts-viewport">
          <div className="experts-track" style={{transform: `translateX(-${cur * 100}%)`}}>
            {list.map((doc, i) => (
              <div className="experts-slide" key={doc.id || doc.name || i} aria-hidden={i !== cur}>
                <DoctorProfileCard doctor={doc} reversed={i % 2 === 1} onBook={onBook}/>
              </div>
            ))}
          </div>
        </div>
        {total > 1 && (
          <div className="experts-nav">
            <button type="button" onClick={() => setCur(p => (p - 1 + total) % total)} aria-label="Previous doctor"><Icon name="chevronLeft" size={18}/></button>
            <div className="experts-dots">
              {list.map((doc, i) => (
                <button key={doc.id || doc.name || i} type="button" className={i === cur ? "active" : ""} onClick={() => setCur(i)} aria-label={`Show ${doc.name || ("doctor " + (i + 1))}`}/>
              ))}
            </div>
            <button type="button" onClick={() => setCur(p => (p + 1) % total)} aria-label="Next doctor"><Icon name="chevronRight" size={18}/></button>
          </div>
        )}
      </div>
    </section>
  );
}

function Gallery() {
  return <section id="smile-gallery" className="section gallery"><SectionHeading eyebrow={site.pages?.gallery?.eyebrow || "VISUAL TOUR & RESULTS"} title={site.pages?.gallery?.title || "Our Smile Gallery & Clinic Experience"} text={site.pages?.gallery?.description || "Explore our sterile, welcoming clinic suites, real patient transformations, and state-of-the-art facilities."}/><div className="gallery-grid">{gallery.map((g,i)=><article className="gallery-card asset-box" key={g.id || g.image || i}>{g.video ? <video src={g.video} controls poster={g.image || undefined}/> : <SmartImage src={g.image} alt={g.title || "Gallery photo"} placeholder={<div className="gallery-placeholder" style={{display:"flex"}}><Icon name="image" size={34}/><span>Upload gallery image in Admin</span></div>}/>}<div className="gallery-overlay"><b>{g.title}</b>{g.text && <p>{g.text}</p>}</div></article>)}</div></section>;
}


function Awards() {
  return (
    <section id="awards" className="section awards-section">
      <SectionHeading
        eyebrow={text("awards.heading.eyebrow", "ACADEMIC HONORS & RECOGNITIONS")}
        title={text("awards.heading.title", "Awards & Scientific Achievements")}
        text={text("awards.heading.text", "Honoring Dr. S. Natesh's distinguished research contributions, forensic odontology achievements, and leadership in dental clinical education.")}
      />

      {awards.length > 0 && <div className="awards-grid">
        {awards.map((award, i) => {
          const year = (String(award.event_date || "").match(/\d{4}/) || [""])[0];
          return (
            <article className="award-card" key={award.id || i}>
              <div className="award-image-wrap">
                <SmartImage
                  src={award.image}
                  alt={award.title || "Award"}
                  placeholder={<div className="gallery-placeholder" style={{ display: "flex" }}><Icon name="award" size={34} /><span>Upload award image in Admin</span></div>}
                />
                {year && <div className="award-badge-pill"><Icon name="award" size={13} /> {year}</div>}
              </div>

              <div className="award-content">
                {award.category && <div className="award-category-tag">{award.category}</div>}
                <h3>{award.title}</h3>
                {award.description && <p className="award-description">{award.description}</p>}

                {(award.venue || award.event_date) && <div className="award-meta-footer">
                  {award.venue && <div className="award-meta-item">
                    <Icon name="map" size={13} />
                    <span>{award.venue}</span>
                  </div>}
                  {award.event_date && <div className="award-meta-item">
                    <Icon name="calendar" size={13} />
                    <span>{award.event_date}</span>
                  </div>}
                </div>}
              </div>
            </article>
          );
        })}
      </div>}
    </section>
  );
}

function OtpModal({otpId,email,preferredDate,expiresIn,resendIn,devOtp,notice,onVerified,onClose,onResend}) {
  const [digits,setDigits]=useState(["","","",""]);
  const [remaining,setRemaining]=useState(expiresIn || 300);   // how long the code stays valid
  const [cooldown,setCooldown]=useState(resendIn || 0);        // wait before another email may be sent
  const [info,setInfo]=useState(notice || "");
  const [error,setError]=useState("");
  const [busy,setBusy]=useState(false);
  const refs=[React.useRef(null),React.useRef(null),React.useRef(null),React.useRef(null)];
  // One interval drives both countdowns so the modal re-renders at most once a second.
  useEffect(()=>{ const t=setInterval(()=>{setRemaining(v=>Math.max(0,v-1));setCooldown(v=>Math.max(0,v-1));},1000); return ()=>clearInterval(t); },[]);
  // The server is the source of truth for both timers.
  useEffect(()=>{ setRemaining(expiresIn || 300); },[expiresIn,otpId]);
  useEffect(()=>{ setCooldown(resendIn || 0); },[resendIn,otpId]);
  useEffect(()=>{ setInfo(notice || ""); },[notice]);
  const value=digits.join("");
  const change=(i,e)=>{ const v=e.target.value.replace(/\D/g,"").slice(-1); const next=[...digits];next[i]=v;setDigits(next);setError("");if(v&&i<3)refs[i+1].current?.focus(); };
  const key=(i,e)=>{if(e.key==='Backspace'&&!digits[i]&&i>0)refs[i-1].current?.focus();};
  const verify=async()=>{if(value.length!==4)return setError("Enter the 4-digit code sent to your Gmail.");if(remaining<=0)return setError("This code has expired. Request a new one.");setBusy(true);setError("");try{await verifyAppointmentOtp({otp_id:otpId,otp:value});onVerified?.();}catch(err){setError(err?.response?.data?.detail||"Verification failed. Please try again.");}finally{setBusy(false);}};
  const resend=async()=>{if(busy)return;setBusy(true);setError("");try{const d=await onResend();setRemaining(d.expires_in||300);setCooldown(d.resend_in||0);setInfo(d.notice||"");setDigits(["","","",""]);setTimeout(()=>refs[0].current?.focus(),0);}catch(err){setError(err?.response?.data?.detail||"Unable to resend the code. Please try again.");}finally{setBusy(false);}};
  const clock=v=>`${String(Math.floor(v/60)).padStart(2,'0')}:${String(v%60).padStart(2,'0')}`;

  const formattedDate = preferredDate ? (() => {
    const parts = String(preferredDate).split("-");
    return parts.length === 3 ? `${parts[2]}/${parts[1]}/${parts[0]}` : preferredDate;
  })() : "";

  return <div className="otp-backdrop" onMouseDown={e=>e.target===e.currentTarget&&onClose?.()}><div className="otp-modal">
    <button className="otp-close" onClick={onClose}><Icon name="x" size={19}/></button>
    <div className="otp-icon"><Icon name="shield" size={23}/></div>
    <span className="otp-step">{text("appointment.otp.step", "STEP 1 OF 2 • INSTANT EMAIL VERIFICATION")}</span>
    <h3>{text("appointment.otp.title", "Verify Your Email Address")}</h3>
    <p className="otp-subtitle">{text("appointment.otp.subtitle", "Enter the 4-digit verification code sent by Gmail to")} <b>{email}</b>.</p>
    <div className="otp-summary"><Icon name="calendar" size={18}/><span>{text("appointment.otp.summary", "Appointment • Preferred Date:")} {formattedDate || "Selected"}</span><button type="button" onClick={onClose}>{text("appointment.otp.edit", "Edit / Change")}</button></div>
    <label className="otp-label">{text("appointment.otp.code_label", "ENTER 4-DIGIT CODE")}</label>
    <div className="otp-boxes">{digits.map((d,i)=><input key={i} ref={refs[i]} autoFocus={i===0} value={d} inputMode="numeric" maxLength={1} onChange={e=>change(i,e)} onKeyDown={e=>key(i,e)} aria-label={`OTP digit ${i+1}`}/>)}</div>
    <div className="otp-timer"><Icon name="clock" size={14}/> {remaining > 0 ? <span>{text("appointment.otp.valid_for", "Code valid for")} <b>{clock(remaining)}</b></span> : <span>{text("appointment.otp.expired", "This code has expired — request a new one.")}</span>}</div>
    <div className="otp-resend"><span>{text("appointment.otp.resend_question", "Didn't receive the code?")}</span>{cooldown > 0 ? <b className="otp-wait">{text("appointment.otp.resend_in", "Resend in")} {clock(cooldown)}</b> : <b className="otp-wait available">{text("appointment.otp.resend_ready", "You can resend now")}</b>}<button type="button" disabled={cooldown>0||busy} onClick={resend}>{busy ? text("appointment.otp.resend_sending", "Sending...") : text("appointment.otp.resend_button", "Resend code")}</button></div>
    <div className="otp-demo"><Icon name="sparkles" size={15}/> <span>{info || (devOtp ? <>{text("appointment.otp.demo_prefix", "Demo code:")} <b>{devOtp}</b></> : text("appointment.otp.sent_note", "One email with your code was sent — check your Gmail inbox and spam folder."))}</span></div>
    {error&&<div className="form-error otp-error">{error}</div>}
    <button className="primary otp-submit" disabled={busy} onClick={verify}><Icon name="shield"/> {busy ? text("appointment.otp.verifying", "Verifying...") : text("appointment.otp.submit", "Verify & Submit Appointment")}</button>
    <div className="otp-secure"><Icon name="phone" size={14} /> {text("appointment.otp.secure", "Secure email verification • Your information is protected")}</div>
  </div></div>;
}

function AppointmentSuccessModal({onClose}) {
  return <div className="appointment-success-backdrop"><div className="appointment-success-toast"><span className="success-check"><Icon name="check" size={22}/></span><div><h4>{text("appointment.success.title", "Appointment Request Received!")}</h4><p>{text("appointment.success.text", "Our patient care team will contact you shortly to confirm.")}</p></div><button onClick={onClose} aria-label="Close"><Icon name="x" size={17}/></button></div></div>;
}

function getTodayLocal() {
  const now = new Date();
  const yyyy = now.getFullYear();
  const mm = String(now.getMonth() + 1).padStart(2, "0");
  const dd = String(now.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

function Appointment({ selectedTreatment = "", onTreatmentChange }) {
  const [sent,setSent]=useState(false);
  const [error,setError]=useState("");
  const [otp,setOtp]=useState(null);
  const [pending,setPending]=useState(null);
  const [formKey,setFormKey]=useState(0);
  const [sending,setSending]=useState(false);

  const submit=async e=>{
    e.preventDefault();
    if(sending) return;
    setError("");
    const form=e.currentTarget;
    if(!form.checkValidity()){ form.reportValidity(); return; }
    const f=new FormData(form);
    const fullName=String(f.get("full_name")||"").trim();
    const mobile=String(f.get("mobile_number")||"").trim();
    const email=String(f.get("email")||"").trim();
    const preferredDateRaw=String(f.get("preferred_date")||"").trim();
    const treatment=String(f.get("treatment_type")||"").trim();
    const normalizedMobile=mobile.replace(/[\s().-]/g, "");
    if(fullName.length < 2) return setError("Please enter your full name (at least 2 characters).");
    if(!/^\+?[0-9]{10,15}$/.test(normalizedMobile)) return setError("Please enter a valid mobile number (10-15 digits).");
    if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return setError("Please enter a valid email address.");
    // Validate dd/mm/yyyy format
    if(!/^\d{2}\/\d{2}\/\d{4}$/.test(preferredDateRaw)) return setError("Please enter the date in dd/mm/yyyy format (e.g. 25/12/2025).");
    const [dd,mm,yyyy]=preferredDateRaw.split("/");
    const parsedDate=new Date(`${yyyy}-${mm}-${dd}`);
    if(isNaN(parsedDate.getTime())) return setError("Please enter a valid date (dd/mm/yyyy).");
    const todayStr=getTodayLocal();
    const enteredStr=`${yyyy}-${mm}-${dd}`;
    if(enteredStr < todayStr) return setError("Please enter today or a future appointment date.");
    const preferredDate=enteredStr; // YYYY-MM-DD for API
    if(!treatment) return setError("Please select a dental service.");
    const payload={full_name:fullName,mobile_number:mobile,email,preferred_date:preferredDate,treatment_type:treatment,message:String(f.get("message")||"").trim()};

    setSending(true);
    try{
      const d=await requestAppointmentOtp(payload);
      setPending(payload);
      setOtp(d);
    }
    catch(err){
      const data = err?.response?.data;
      let msg = "";
      if (typeof data === "string") msg = data;
      else if (data?.detail) msg = data.detail;
      else if (typeof data === "object") {
        msg = Object.entries(data).map(([k,v])=>`${k}: ${Array.isArray(v)?v.join(', '):v}`).join(" | ");
      }
      setError(msg || err?.message || "Unable to send verification code right now.");
    }
    finally{ setSending(false); }
  };

  const resend=async()=>{ const d=await requestAppointmentOtp(pending); setOtp(d); return d; };
  const verified=()=>{ setOtp(null); setPending(null); setSent(true); setFormKey(k=>k+1); };

  return <section id="appointment" className="appointment">
    <div className="appointment-copy">
      <span className="eyebrow light"><Icon name="calendar" size={13} style={{ marginRight: 5, verticalAlign: "middle" }} /> {site.pages?.appointment?.eyebrow || "EASY ONLINE BOOKING"}</span>
      <h2>{site.pages?.appointment?.title || "Schedule Your Smile Consultation"}</h2>
      <p>{site.pages?.appointment?.description || "Take the first step towards exceptional oral wellness. Select your preferred date and treatment, and our patient coordinator will confirm in less than 15 minutes."}</p>
      <ul>
        <li><Icon name="check"/> {text("appointment.bullet_1", "Personalized initial consultation for new patients")}</li>
        <li><Icon name="clock"/> {text("appointment.bullet_2", "Instant Email verification & calendar confirmation")}</li>
        <li><Icon name="phone"/> {text("appointment.bullet_3", `Prefer calling? ${branchPhoneText()}`)}</li>
      </ul>
    </div>
    <form key={formKey} className="booking-card" onSubmit={submit} noValidate={false}>
      <h3>{text("appointment.form_title", "Book Your Appointment")}</h3><p>{text("appointment.form_subtitle", "Fill in the details below to request a convenient time slot.")}</p>
      <div className="form-grid">
        <Field name="full_name" label={text("appointment.field.name.label", "FULL NAME *")} placeholder={text("appointment.field.name.placeholder", "John Doe")} icon="user" autoComplete="name" minLength={2} maxLength={100}/>
        <Field name="mobile_number" label={text("appointment.field.mobile.label", "MOBILE NUMBER *")} placeholder={text("appointment.field.mobile.placeholder", "+91 98765 43210")} icon="phone" type="tel" autoComplete="tel" minLength={10} maxLength={20} pattern="[0-9+()\-\s]{10,20}"/>
        <Field name="email" label={text("appointment.field.email.label", "EMAIL ADDRESS *")} placeholder={text("appointment.field.email.placeholder", "john@example.com")} icon="mail" type="email" autoComplete="email" maxLength={254}/>
        <PreferredDateField name="preferred_date" label={text("appointment.field.date.label", "PREFERRED DATE *")} placeholder={text("appointment.field.date.placeholder", "dd/mm/yyyy")}/>
        <label className="field full"><span>{text("appointment.field.message.label", "ADDITIONAL MESSAGE OR SYMPTOMS")}</span><textarea name="message" placeholder={text("appointment.field.message.placeholder", "Tell us if you have toothache, sensitivity, or specific goals...")} maxLength={1000}/></label>
        <label className="field"><span>{text("appointment.field.treatment.label", "TREATMENT TYPE *")}</span><div className="select treatment-select"><span className="select-icon"><Icon name="heart"/></span><select name="treatment_type" required value={selectedTreatment || ""} onChange={(e) => onTreatmentChange?.(e.target.value)} aria-label="Treatment Type"><option value="" disabled>{text("appointment.field.treatment.placeholder", "Select Dental Service")}</option>{services.map(s=><option key={s.id || s.title} value={s.title}>{s.title}</option>)}</select><span className="select-chevron"><Icon name="chevron"/></span></div></label>
      </div>
      <button className="primary submit" type="submit" disabled={sending}><Icon name="calendar"/> {sending ? "Sending verification code..." : text("appointment.submit", "Confirm & Book Appointment")}</button>{error && <div className="form-error">{error}</div>}<small className="privacy"><Icon name="phone" size={14} /> {text("appointment.privacy", "Your information is securely verified by email before the appointment is created.")}</small>
    </form>
    {sent&&<AppointmentSuccessModal onClose={()=>setSent(false)}/>}
    {otp&&<OtpModal otpId={otp.otp_id} email={otp.masked_email} preferredDate={pending?.preferred_date} expiresIn={otp.expires_in} resendIn={otp.resend_in} devOtp={otp.dev_otp} notice={otp.notice} onVerified={verified} onClose={()=>setOtp(null)} onResend={resend}/>}
  </section>;
}

// `name` is passed explicitly so the visible label can be reworded in Admin
// without ever changing the field name the booking form submits.
function Field({name,label,placeholder,icon,type="text",autoComplete,minLength,maxLength,pattern,min,inputMode}) {
  return <label className="field"><span>{label}</span><div><Icon name={icon}/><input name={name} required placeholder={placeholder} type={type} autoComplete={autoComplete} minLength={minLength} maxLength={maxLength} pattern={pattern} min={min} inputMode={inputMode}/></div></label>;
}

// Preferred Date still submits dd/mm/yyyy (the API and the validation above
// expect that format), but the calendar icon pops the browser's native date
// picker. The chosen yyyy-mm-dd value is reformatted into the text input, so
// patients can use the picker or keep typing the date by hand.
function PreferredDateField({name,label,placeholder}) {
  const [value,setValue]=useState("");
  const pickerRef=useRef(null);

  const openPicker=()=>{
    const el=pickerRef.current;
    if(!el) return;
    // showPicker() is the only way to open the calendar from a button; it needs
    // the transient user activation we still have here. Fall back to focus().
    if(typeof el.showPicker==="function"){
      try{ el.showPicker(); return; }catch{ /* fall through */ }
    }
    el.focus();
  };

  const pick=e=>{
    const iso=e.target.value; // yyyy-mm-dd
    if(!iso) return;
    const [yyyy,mm,dd]=iso.split("-");
    setValue(`${dd}/${mm}/${yyyy}`);
  };

  return <label className="field"><span>{label}</span><div className="date-field"><span role="button" tabIndex={0} className="date-icon-btn" aria-label="Open calendar picker" onClick={e=>{ e.preventDefault(); openPicker(); }} onKeyDown={e=>{ if(e.key==="Enter"||e.key===" "){ e.preventDefault(); openPicker(); } }}><Icon name="calendar"/></span><input name={name} required type="text" placeholder={placeholder} pattern="\d{2}/\d{2}/\d{4}" inputMode="numeric" value={value} onChange={e=>setValue(e.target.value)}/><input ref={pickerRef} className="date-picker-input" type="date" tabIndex={-1} aria-hidden="true" min={getTodayLocal()} onChange={pick}/></div></label>;
}

// Google Maps links for every clinic branch. The first address is the primary
// location (embedded map + main button); any extra addresses become waypoints so
// one click still routes to all of them. Each address also gets its own link.
const MAPS_FALLBACK_ADDRESS = "Mount Dental Care, Chennai, Tamil Nadu, India";
function directionsLink(addresses) {
  const list = (addresses || []).filter(Boolean);
  if (!list.length) list.push(MAPS_FALLBACK_ADDRESS);
  const [primary, ...rest] = list;
  const params = new URLSearchParams({ api: "1", destination: primary });
  if (rest.length) params.set("waypoints", rest.join("|"));
  return `https://www.google.com/maps/dir/?${params}`;
}
function mapSearchLink(address) {
  return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(address || MAPS_FALLBACK_ADDRESS)}`;
}

function Contact() {
  const addresses = site.addresses?.filter(Boolean)?.length ? site.addresses.filter(Boolean) : [MAPS_FALLBACK_ADDRESS];

  // Branch maps come from Django Admin (CMS -> Branches). Only branches that
  // have an embed URL are mapped, so adding a location in Admin adds a map too.
  const branchMaps = branches.filter(b => b.map_embed_url);
  const phoneLine = branchPhoneText();

  return <section id="contact" className="contact section">
    <div className="contact-copy">
      <span className="eyebrow">{site.pages?.contact?.eyebrow || "GET IN TOUCH"}</span>
      <h2>{site.pages?.contact?.title || "We'd Love to Welcome You"}</h2>
      <p>{site.pages?.contact?.description || "Conveniently located with dedicated patient parking, accessible transit links, and friendly reception support."}</p>
      <ContactItem icon="phone" title={text("contact.call_label", "CALL DIRECTLY")} value={phoneLine} />
      <ContactItem icon="mail" title={text("contact.email_label", "EMAIL SUPPORT")} value={site.email || "mountdentalcare@gmail.com"} />
      <div className="contact-item address">
        <span className="contact-icon yellow"><Icon name="map" /></span>
        <div style={{ flex: 1 }}>
          <small>{text("contact.locations_label", "CLINIC LOCATIONS")}</small>
          <div className="contact-address-list">
            {addresses.map((a, i) => (
              <div key={`${i}-${a}`} className="contact-address-item">
                <span>{a}</span>
                <a className="address-directions" href={mapSearchLink(a)} target="_blank" rel="noreferrer" aria-label={`Get directions to ${a}`}>
                  <Icon name="send" size={12} /> {text("contact.directions", "Get Directions")}
                </a>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
    <div className="map-card exact-map-card">
      {branchMaps.length > 0 && <div className="dual-map-grid">
        {branchMaps.map((branch) => (
          <div className="branch-map-wrap" key={branch.id || branch.name}>
            <div className="branch-map-label">
              <span className="map-live-dot" />
              <b>{branch.name}</b>
            </div>
            <div className="map-frame branch-map-frame">
              <iframe
                title={branch.name || "Clinic map"}
                src={branch.map_embed_url}
                loading="lazy"
                referrerPolicy="no-referrer-when-downgrade"
                allowFullScreen
              />
            </div>
            <div className="branch-map-footer">
              {branch.address && <small>{branch.address}</small>}
              <a className="map-directions" href={branch.map_directions_url || mapSearchLink(branch.address)} target="_blank" rel="noreferrer">
                <Icon name="send" size={13} /> {text("contact.directions", "Get Directions")}
              </a>
            </div>
          </div>
        ))}
      </div>}
    </div>
  </section>;
}

function ContactItem({icon,title,value}) { return <div className="contact-item"><span className="contact-icon"><Icon name={icon}/></span><div><small>{title}</small><b>{value}</b></div></div> }

const DEFAULT_FOOTER_LINKS = [
  { group: "quick", label: "About Our Clinic", url: "#about-clinic" },
  { group: "quick", label: "Our Doctors & Team", url: "#our-dentists" },
  { group: "quick", label: "Smile Gallery & Results", url: "#smile-gallery" },
  { group: "quick", label: "Why Choose Us", url: "#why-choose-us" },
  { group: "treatments", label: "Laser Teeth Whitening", url: "#services" },
  { group: "treatments", label: "Dental Implants (Titanium & Zirconia)", url: "#services" },
  { group: "treatments", label: "Clear Aligners & Braces", url: "#services" },
  { group: "treatments", label: "Painless Root Canal Treatment", url: "#services" },
  { group: "treatments", label: "Porcelain Cosmetic Veneers", url: "#services" },
  { group: "treatments", label: "Children's Pediatric Care", url: "#services" }
];
const DEFAULT_HOURS = [
  { day: "Mon - Sat", hours: "Morning - 10.00 AM - 01.00 PM | Evening 05.00 PM - 08.30 PM", emergency: false },
  { day: "St.Thomas Mount - 044-2234 5000", hours: "Nungambakkam - 044-2827 5000", isContact: true, emergency: false }
];

function Footer({ onCall }) {
  // Use the Admin-managed footer links and clinic hours when present, so a
  // change saved in Django Admin shows up on the site.
  const adminFooter = site.footer?.length ? site.footer : DEFAULT_FOOTER_LINKS;
  const primaryBranch = branchLabel(branches[0]) || "St.Thomas Mount - 044-2234 5000";
  const secondaryBranch = branchLabel(branches[1]) || "Nungambakkam - 044-2827 5000";
  // The footer blurb is edited in Admin (Site Settings -> Top Bar & Footer).
  const quickLinks = adminFooter.filter(x => x.group === "quick");
  const treatmentLinks = adminFooter.filter(x => x.group === "treatments");
  const rawHours = site.hours?.length ? site.hours : DEFAULT_HOURS;
  const hours = rawHours.map(h => {
    let day = h.day || "";
    let val = h.hours || "";
    if (typeof val === "string") {
      val = val.replace("Morning - 10.00 AM - 01.00 PM, Evening", "Morning - 10.00 AM - 01.00 PM | Evening");
    }
    if (day === "Sunday" || (typeof val === "string" && val.includes("By Appointment Only"))) {
      return { isContact: true, branch1: primaryBranch, branch2: secondaryBranch };
    }
    if (day.includes("St.Thomas Mount") || val.includes("Nungambakkam")) {
      return {
        isContact: true,
        branch1: day.includes("St.Thomas Mount") ? day : primaryBranch,
        branch2: val.includes("Nungambakkam") ? val : secondaryBranch
      };
    }
    return { ...h, hours: val };
  });

  return (
    <footer className="footer">
      <div className="footer-top">
        <div className="footer-brand">
          <div className="footer-logo-wrap"><Logo alt={`${site.clinic || "Mount Dental Care"} logo`} /></div>
          <p>{site.footerAbout || "Providing exceptional, patient-first dental treatments with cutting-edge technology and genuine human warmth. Your smile is our lifelong masterpiece."}</p>
        </div>
        <div>
          <h4>{text("footer.quick_links_title", "QUICK LINKS")}</h4>
          {quickLinks.map(x => <a key={x.label} href={x.url || "#home"}>{x.label}</a>)}
        </div>
        <div>
          <h4>{text("footer.treatments_title", "KEY TREATMENTS")}</h4>
          {treatmentLinks.map(x => <a key={x.label} href={x.url || "#services"}>{x.label}</a>)}
        </div>
        <div>
          <h4>{text("footer.hours_title", "CLINIC HOURS")}</h4>
          <div className="hours">
            {hours.map((h, idx) => {
              if (h.isContact) {
                return (
                  <div className="hours-row hours-contact-row" key={idx}>
                    {[h.branch1, h.branch2].filter(Boolean).map((label, i) => {
                      const { name, phone } = splitBranchLabel(label);
                      return (
                        <span className="hours-branch" key={`${label}-${i}`}>
                          {name}{phone ? ` - ${phone}` : ""}
                        </span>
                      );
                    })}
                  </div>
                );
              }
              return (
                <div className="hours-row" key={h.day || idx}>
                  <span className="hours-day">{h.day}</span>
                  <span className={`hours-val ${h.emergency ? 'highlight' : ''}`}>{h.hours}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
      <div className="footer-bottom">
        <span>{copyrightLine()}</span>
        <span className="footer-credit">
          <a href="https://vetriitsystems.com/" target="_blank" rel="noopener noreferrer">Designed &amp; Developed by Vetri IT Systems</a>
        </span>
      </div>
    </footer>
  );
}

export default function App() {
  const [cmsVersion, setCmsVersion] = useState(0);
  const [selectedTreatment, setSelectedTreatment] = useState("");
  const [showPhoneModal, setShowPhoneModal] = useState(false);
  const book=(treatment)=>{
    if (typeof treatment === "string" && treatment) {
      setSelectedTreatment(treatment);
    }
    setTimeout(()=>document.getElementById("appointment")?.scrollIntoView({behavior:"smooth",block:"start"}),0);
  };
  const handleCall = () => setShowPhoneModal(true);

  useEffect(()=>{
    let mounted = true;
    let lastPayload = "";
    const refreshCms = async () => {
      try {
        const data = await loadSite();
        const fingerprint = JSON.stringify(data);
        // Only re-render when Admin content actually changed, and re-render
        // instead of remounting so an open booking form / OTP popup survives
        // the 10-second CMS refresh.
        if (fingerprint === lastPayload) return;
        lastPayload = fingerprint;
        hydrateFromBackend(data);
        if (mounted) setCmsVersion(v => v + 1);
      } catch (error) {
        console.warn("Unable to load CMS data from Django:", error);
      }
    };
    refreshCms();
    const timer = window.setInterval(refreshCms, 10000);
    const onFocus = () => refreshCms();
    window.addEventListener("focus", onFocus);
    return () => {
      mounted = false;
      window.clearInterval(timer);
      window.removeEventListener("focus", onFocus);
    };
  },[]);

  return <div className="app-root">
    <Header onBook={book} onCall={handleCall}/><Hero onBook={book} onCall={handleCall}/><Offer onBook={book}/><Services onBook={book}/><WhyChoose/><About/><Experts onBook={book}/><Gallery/><Awards/><Appointment selectedTreatment={selectedTreatment} onTreatmentChange={setSelectedTreatment}/><Contact/><Footer onCall={handleCall}/>
    {/* Rendered at the app root so the fixed position and z-index are not
        trapped inside a section's stacking context. */}
    <FloatingActions onCall={handleCall}/>
    {showPhoneModal && <PhoneSelectorModal onClose={() => setShowPhoneModal(false)} />}
  </div>;
}

