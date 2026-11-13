"""YouTube videos from @DrSobtiDental used on this site (shared list with the other two clinic sites)."""
# Shared YouTube video data for all three sites. Titles are cleaned (no hashtags/emoji); summaries are ours, built from each video's own description.
# fields: id, kind (video|short), title, date, duration (m:ss), lang, summary
V = {}
def v(id, kind, date, dur, title, summary, lang="en"):
    V[id] = dict(id=id, kind=kind, date=date, dur=dur, title=title, summary=summary, lang=lang)

# --- implants: Dr Pushkar Ke Pravachan series and explainers
v("dYEhKOXOMzs","short","2026-07-29","0:41","Why an intraoral scan matters for dental implants (Episode 2)","Dr Pushkar Sobti explains how a digital intraoral scan makes a 3D model of your teeth, helps plan implant position and improves the fit of the final teeth.")
v("p9j2WCe0snU","short","2026-07-29","0:57","How CBCT and intraoral scans plan implant surgery (Episode 3)","How the CBCT scan and the intraoral scan are combined to plan the implant position, design the new tooth before surgery and guide placement.")
v("yDUGyAIrIkY","short","2026-07-31","1:16","Expensive vs cheap dental implants: what is the difference?","Why implant price alone is a poor guide: results depend on the whole system, the planning, the surgery, the crown design and long-term maintenance.", "hi")
v("9M_-cY1hOkc","short","2026-08-01","1:02","An implant is not just a screw: what is an abutment? (Episode 6)","The abutment connects the implant to the crown. Dr Pushkar explains custom abutments and why titanium grade 5 is used.", "hi")
v("P72CUlyTOoU","short","2026-08-03","0:54","Bone grafting before dental implants: do you need it? (Episode 7)","What bone grafting is, when it is needed before an implant, and how it builds enough jawbone when the CBCT scan shows too little.")
v("xzKng09DQMI","short","2026-08-04","0:47","Can dental implants fail years later? Warning signs (Episode 8)","The warning signs of implant problems, why they happen and how to look after an implant so it lasts.")
v("HWms2lCr5kk","short","2026-08-05","1:05","Free-hand vs guided implant surgery (Episode 9)","The difference between free-hand and computer-guided implant surgery, and why a CBCT-based plan and a surgical guide add precision.")
v("Ssyi8Ww8Hzo","short","2026-08-06","0:37","Can you get dental implants if you take blood thinners? (Episode 10)","Being on blood thinners does not rule out implants. The dentist plans with your cardiologist or physician and gets written medical clearance first.")
v("4VYjcgqGHm0","short","2026-08-07","0:52","Can diabetic patients get dental implants? HbA1c explained (Episode 11)","What HbA1c is, why it is checked before implant surgery, how diabetes affects healing and the precautions taken for diabetic patients.")
v("Ee7Kt0J5CbQ","short","2026-08-08","0:32","Is there an age limit for dental implants? (Episode 12)","Age alone rarely decides it. General health, bone, healing ability and medical history matter more, for younger and older patients alike.")
v("GdJIYnfavNk","short","2026-08-10","0:54","How nerve injury is avoided during implant placement (Episode 13)","How the nerve is located on the CBCT scan, and how guided planning, the right angle and the right depth keep implant surgery safe.", "hi")
v("IROlKXqTJ68","short","2026-10-22","0:59","What is a CBCT scan? 3D dental scanning explained","Dr Pushkar Sobti explains cone beam CT: the 3D scan that shows teeth, jawbone and nearby structures before treatment.")
v("y6bjdsXc5Co","short","2026-07-28","0:31","Why every implant patient needs a CBCT scan first","A flat X-ray cannot show bone width, nerves and sinuses. A CBCT scan shows them in 3D, so the implant can be placed safely.")
v("WWQTpD7TeyA","short","2026-07-30","0:59","Immediate vs delayed dental implants: when is the best time?","When an implant can go in on the day of the extraction, when it is better to wait, and how the right timing protects bone and gums.")
v("FISGsq9ISaY","short","2026-09-20","2:31","Dental implant treatment explained, step by step","The implant process at Dr Sobti's Dental Care, Rajouri Garden: diagnosis, CBCT planning, intraoral scan, guided placement and the final crown.")
v("iT-obTL8EGY","video","2026-09-24","0:34","One missing tooth: dental implant or bridge?","A bridge needs the neighbouring teeth to be cut down; an implant replaces the tooth on its own. Which is better depends on bone, neighbouring teeth and bite.", "hi")
# --- implants: cases
v("d_gSJVCSRy8","short","2026-05-13","0:39","Missing teeth? All-on-X fixed teeth on implants","All-on-X gives a full fixed set of teeth on implants: a titanium framework with zirconia teeth, not removable like a denture.")
v("mUrHLsgGRT8","short","2026-04-21","0:10","A full mouth implant case, start to finish","Assessment, implant placement, scan body records, trial, layering and final delivery of a titanium and ceramic full-arch bridge, all in-house.")
v("yRsgb20K6gc","video","2026-10-09","0:26","Osstem OneArch scan body in a full-arch implant case","Scan bodies record the exact implant positions in an All-on-X case so the full-arch bridge can be designed digitally and fit accurately.")
v("wo9KHKKsgRI","video","2026-06-06","1:05","Guided dental implant placement","CBCT scan and digital planning place the implant around bone, nerve and sinus; a printed surgical guide carries the plan into the mouth.")
v("8nA4r3d-Gt0","short","2026-03-10","0:33","Guided implant with a fixed crown the same day","CBCT planning and guided surgery with a Nobel Biocare implant let this patient leave with a fixed crown on the same day.")
v("mbwAgZtrRoo","video","2026-04-27","1:42","Failing lower front teeth replaced with immediate implants","Extraction, immediate implant placement, digital planning and the final bridge from the in-house lab for failing lower front teeth.")
v("XTkuO0cxLKw","short","2026-07-28","0:41","She thought it was just a cap: a dental implant story","An old cap hid a tooth that could not be saved. The X-ray found it, and an implant replaced the tooth.")
v("3rPYx82hlhk","short","2026-03-13","0:29","Custom titanium implant abutment, made in-house","From digital scan to CAD-CAM design and titanium milling: a custom abutment for a better fit and a natural-looking crown.")
# --- implants: patient stories
v("mOf8SY1nW9Y","short","2026-09-20","0:44","Dental implant patient testimonial","A patient describes their dental implant treatment at Dr Sobti's Dental Care, Rajouri Garden, from consultation to the final tooth.")
v("8W8GF76DnyA","short","2026-03-14","0:58","A patient from Singapore on her dental implants","A patient who travelled from Singapore to Delhi for dental implants shares her experience of the treatment.")
v("_LgsARouKa0","short","2026-04-11","1:17","Years of trust: a patient who flies in from abroad","A long-time patient who travels from abroad describes his painless dental implant treatment.")
# --- smile design / general (drparulssobti.com)
v("6PXXzwvCBco","short","2026-08-11","0:16","A smile makeover that keeps the teeth's character","A natural-looking smile transformation from Dr Sobti's Dental Care, Rajouri Garden.")
v("etx9YUTW_kg","short","2026-07-25","0:54","He hid his smile for years: smile transformation","A cosmetic dentistry case that restored a patient's confidence to smile.")
v("oAl3H6l39Es","short","2026-04-04","1:39","\"I smile a lot now\": smile designing for discoloured teeth","A patient talks about her smile designing treatment, which corrected discoloured teeth.")
v("s3GXnZ2gkUk","short","2026-03-25","0:49","Composite veneers after a root canal","Minimally invasive composite veneers reshaped this patient's smile after root canal treatment.")
v("t2iKVdDL8D0","short","2026-04-06","0:23","A broken front tooth fixed in two visits","A 12-year-old with a tooth broken at school: root canal treatment and a freehand composite veneer in two sittings.")
v("2_e0jS8wVsg","short","2026-03-17","0:40","She wanted the same tooth back, in 2 hours","A same-day crown designed with the patient, to match her own tooth.")
v("1SivMyXkBa0","short","2026-03-31","0:23","Smile design, part 1: guess what this is becoming","Part 1: the new teeth being designed and milled in the clinic's lab.")
v("VBxecBKQiYo","short","2026-04-01","0:27","Smile design, part 2: the making","Part 2: the restoration being finished before the reveal.")
v("6zl3kROUoso","short","2026-04-08","0:19","Smile design, part 3: the final reveal","Part 3: the finished smile.")
v("fvKcdFYR3R8","short","2026-08-09","0:13","Digital crown design, from scan to final crown","A dental crown designed on screen, milled and finished in the clinic's lab.")
v("K6o1xrWnsJ4","short","2026-03-16","0:46","A 10-year-old's root canal, from fear to a smile","Jaitik, 10, shares how he felt during his root canal treatment.")
v("HMKI76NpUCw","short","2026-03-21","0:51","From fear to fearless: a child's dental visit","How a nervous child became comfortable at the clinic and completed his treatment.")
v("4pk7Kov41sQ","short","2026-08-02","0:37","Choosing the right dentist for your child","A father talks about bringing his daughter for treatment.")
v("kQDuNdLutes","short","2026-03-27","0:16","Scared of the dentist? Laughing gas sedation","Nitrous oxide (laughing gas) helps anxious patients relax during treatment.")
v("a3YGzvm1YsU","short","2026-07-21","0:26","Scared of wisdom tooth removal? A patient's view","A patient describes her wisdom tooth extraction.")
v("kPXjCugNphI","short","2026-03-28","1:05","Saving fractured back teeth with root canal treatment","Painless root canal treatment saved a patient's fractured back teeth.")
v("Vu4W2Kl_Mvs","short","2026-04-22","0:13","Gentler gum treatment with the Woodpecker PT-A","Periodontal (gum) cleaning with a newer, gentler ultrasonic system.")
v("Q4XgYfekrpw","short","2026-09-28","0:40","Air polishing and pain-free cleaning: Rahul's story","A patient travels from Greater Noida for pain-free dental air polishing and cleaning.")
# --- implants: November 2026 (on dentalimplantsdelhi.com/videos/; the long bone grafting video has its own page there)
v("LQ7iloK2d2s","short","2026-11-05","0:26","Immediate dental implants: same-day teeth explained","When an implant can go in on the day the tooth comes out, and what decides it.")
v("4SWuUtidiY0","video","2026-11-06","","Bone grafting for dental implants: is it necessary?","Most patients do not need a bone graft; the CBCT scan shows when one is needed.")
v("3MrBCvGjHCM","short","2026-11-09","0:40","Why a CBCT scan is important for dental implants","A 3D scan shows bone, nerve and sinus so the implant can be planned before surgery.")
v("W6RcpeG_Wi8","short","2026-11-10","0:56","Full-mouth implants for a medically compromised patient","A full-mouth case planned with the patient's physician, in Hindi.", "hi")
v("WzzNP5tw_uk","short","2026-11-12","0:19","Does a dental implant feel like a real tooth?","Dr Pushkar Sobti answers in Hindi.", "hi")
# --- clinic (sobtidentalcare.com)
v("thmGh27-57I","short","2026-03-20","0:56","Our story: from 288 to 4,500 square feet","Dr Pushkar Sobti and Dr Parul Sobti on how the Rajouri Garden clinic grew.")
v("lDd7hbX0E9k","short","2026-07-24","0:54","Clinic tour: Dr Sobti's Dental Care, Rajouri Garden","Reception, treatment rooms and the digital dentistry set-up.")
v("VL64ySkZs60","short","2026-08-06","0:10","Inside Dr Sobti's Dental Care","A quick look inside the Rajouri Garden clinic.")
v("u_y8lzaJhoQ","short","2026-04-07","0:41","Setting up a treatment room for the next patient","How a room is cleaned and prepared between patients.")
v("YsTfqx1xLLM","short","2026-09-23","1:32","Patient testimonial: treatment at Dr Sobti's Dental Care","A patient describes the doctors, the clinic and the care they received.")
v("kRn6ixupOLc","short","2026-05-06","0:25","Our Roland DWX-52D Plus milling machine","The in-house lab's milling machine for zirconia and PMMA crowns, bridges and implant teeth.")
v("nkUCoO-IgKk","short","2026-03-11","0:46","A zirconia bridge made in-house, scan to delivery","Intraoral scan, design, milling, sintering, staining and glazing of a monolithic zirconia bridge.")

def iso(d):
    if not d:
        return ""
    m, s = d.split(":"); return f"PT{int(m)}M{int(s)}S" if int(m) else f"PT{int(s)}S"

def obj(x, page_url):
    return {k: v for k, v in _obj(x).items() if v}

def _obj(x):
    return {"@type": "VideoObject", "name": x["title"], "description": x["summary"],
            "thumbnailUrl": f"https://i.ytimg.com/vi/{x['id']}/hqdefault.jpg",
            "uploadDate": x["date"] + "T10:00:00+05:30", "duration": iso(x["dur"]),
            "embedUrl": f"https://www.youtube.com/embed/{x['id']}",
            "url": f"https://www.youtube.com/{'shorts/' + x['id'] if x['kind']=='short' else 'watch?v=' + x['id']}",
            "inLanguage": "hi-IN" if x["lang"] == "hi" else "en-IN"}

def card(x, esc):
    url = f"https://www.youtube.com/{'shorts/' + x['id'] if x['kind']=='short' else 'watch?v=' + x['id']}"
    return (f'<figure class="yt-card {x["kind"]}"><a class="yt" href="{url}" data-id="{x["id"]}" rel="noopener">'
            f'<img src="https://i.ytimg.com/vi/{x["id"]}/hqdefault.jpg" alt="{esc(x["title"])}" loading="lazy" width="480" height="360">'
            f'<span class="yt-play" aria-hidden="true"></span><span class="yt-time">{x["dur"]}</span></a>'
            f'<figcaption><strong>{esc(x["title"])}</strong><span>{esc(x["summary"])}</span></figcaption></figure>')

CSS = """.yt-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,13.5rem),1fr));gap:1.25rem;margin:1rem 0 0}
.yt-card{margin:0;display:flex;flex-direction:column;gap:.55rem;min-width:0}
.yt-card .yt,.yt-card iframe{position:relative;display:block;width:100%;aspect-ratio:9/16;border-radius:10px;overflow:hidden;background:#0b1530;border:0}
.yt-card.video .yt,.yt-card.video iframe{aspect-ratio:16/9}
.yt-card img{width:100%;height:100%;object-fit:cover;display:block}
.yt-play{position:absolute;left:50%;top:50%;width:3.4rem;height:3.4rem;margin:-1.7rem 0 0 -1.7rem;border-radius:50%;background:rgba(30,78,162,.92);box-shadow:0 4px 18px rgba(0,0,0,.35)}
.yt-play::after{content:"";position:absolute;left:1.3rem;top:1rem;border-style:solid;border-width:.7rem 0 .7rem 1.15rem;border-color:transparent transparent transparent #fff}
.yt:hover .yt-play{background:#f0b04f}
.yt-time{position:absolute;right:.5rem;bottom:.5rem;background:rgba(0,0,0,.72);color:#fff;font-size:.75rem;padding:.1rem .4rem;border-radius:4px}
.yt-card figcaption{display:flex;flex-direction:column;gap:.25rem;font-size:.92rem;line-height:1.4}
.yt-card figcaption span{color:var(--muted,#5b6475);font-size:.86rem}"""

JS = """<script>
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a.yt[data-id]');if(!a)return;e.preventDefault();
var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+a.dataset.id+'?autoplay=1&rel=0';f.title=a.querySelector('img').alt;
f.allow='accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture';f.allowFullscreen=true;a.replaceWith(f);});
</script>"""
