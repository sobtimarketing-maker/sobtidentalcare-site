"""General dentistry pages on the hub (Dr, 22 Nov 2026: drparulssobti.com is only smile design, cosmetics and
veneers; dentalimplantsdelhi.com only implants; everything else lives here).

Moved from drparulssobti.com on 22 Nov 2026 with the same file names, so the redirects there carry the Google
rankings over. Prices (Dr, 22 Nov 2026): only basic STARTING prices ("From ₹...") that were already published; never exact costs
and no new prices. Pages without "prices" (kids, wisdom tooth) show a WhatsApp/call cost box instead.
Exact cost is given only after the patient is examined.
Fields: slug, wa (treatment named in the WhatsApp message), name, title, desc, label, h1, intro, prices [(item, starting price)] (optional),
sections [(heading, [paragraph or list of bullets])], facts [(label, value)], faq [(question, answer)], cta.
"""

GENERAL_PAGES = [{'slug': 'dental-crown-cost-delhi.html',
  'wa': 'Crowns',
  'name': 'Dental crowns',
  'title': "Dental Crown (Teeth Cap) Cost in Delhi: Zirconia from ₹8,000 | Dr Sobti's Dental Care",
  'desc': 'Teeth cap price in Delhi: zirconia crowns from ₹8,000 and E-max crowns from ₹10,000 per tooth, made in '
          'our in-house lab with a warranty. Same-day crowns in Rajouri Garden.',
  'label': 'Treatments · Crowns and caps',
  'h1': 'Dental crown (teeth cap) cost in Delhi',
  'intro': "Metal-free zirconia and E-max crowns, made in the clinic's own lab at Dr Sobti's Dental Care, Rajouri "
           'Garden. If you are checking dental crown cost in Delhi, our zirconia crowns start from ₹8,000 per tooth.',
  'prices': [('Zirconia crown', 'From ₹8,000 per tooth'),
             ('E-max (glass ceramic) crown', 'From ₹10,000 per tooth'),
             ('Dental bridge', 'Crown price × number of teeth in the bridge')],
  'sections': [('Which crown is right for you',
                ["We only make metal-free crowns. They look like natural teeth and don't leave a dark line at the "
                 'gum.',
                 ['Zirconia is very strong, so it suits back teeth and people who grind.',
                  'E-max is a glass ceramic that lets light through like enamel, so it is a favourite for front '
                  'teeth.'],
                 'Dr Parul will tell you which material suits each tooth before you decide.']),
               ('What a bridge costs',
                ['A bridge replaces a missing tooth by joining crowns on the teeth either side. The cost depends on '
                 'how many teeth the bridge covers and the material you choose.',
                 'If you would rather not cut down the neighbouring teeth, a <a '
                 'href="https://dentalimplantsdelhi.com/dental-implant-cost-delhi/">dental implant</a> may be the '
                 'better choice.']),
               ('Same-day crowns from our own lab',
                ['Your tooth is scanned with an intraoral scanner instead of messy impressions. Glass-ceramic crowns '
                 'can be milled in our in-house lab and fitted the same day. Every crown comes with a warranty. See '
                 '<a href="/same-day-dentistry-rajouri-garden.html">same-day dentistry</a>.'])],
  'facts': [('Zirconia', 'From ₹8,000 per tooth'),
            ('E-max', 'From ₹10,000 per tooth'),
            ('Materials', 'Zirconia and E-max, metal-free'),
            ('Made in', 'Our own lab, same floor'),
            ('Same day', 'Glass-ceramic crowns'),
            ('Warranty', 'On every crown')],
  'faq': [('What is the price of a teeth cap in Delhi?',
           "At Dr Sobti's Dental Care in Rajouri Garden, a zirconia cap starts from ₹8,000 per tooth and an E-max "
           'cap from ₹10,000 per tooth. Both are metal-free and come with a warranty.'),
          ('How much does a zirconia crown cost?',
           'Zirconia crowns start from ₹8,000 per tooth. They are made in our in-house lab.'),
          ('Why does tooth cap cost in India vary so much?',
           'Mostly because of the material and the lab behind it. A metal cap from an outside lab costs far less '
           'than a zirconia or E-max crown milled to fit, and zirconia crown cost in India also depends on the brand '
           'of zirconia used. Ask any clinic what material you are paying for. Ours are all metal-free.'),
          ('Do you make metal or metal-ceramic crowns?',
           'No. We only make metal-free crowns: zirconia and E-max glass ceramic.'),
          ('Can I get a crown in one day?',
           'Yes, glass-ceramic crowns can be made and fitted the same day, because they are milled in our own lab.'),
          ('How much does a dental bridge cost in Delhi?',
           'Multiply the crown price by the number of teeth in the bridge. A three-unit zirconia bridge starts from '
           '₹24,000.')],
  'cta': 'Book a crown consultation'},
 {'slug': 'braces-cost-delhi.html',
  'wa': 'Braces',
  'name': 'Braces',
  'title': "Braces Cost in Delhi: Metal from ₹40,000, Ceramic from ₹50,000 | Dr Sobti's Dental Care",
  'desc': "Teeth braces cost in Delhi at Dr Sobti's Dental Care, Rajouri Garden: metal braces from ₹40,000, ceramic "
          'from ₹50,000, self-ligating from ₹60,000. For children and adults.',
  'label': 'Treatments · Braces',
  'h1': 'Braces cost in Delhi',
  'intro': "Metal, ceramic and self-ligating braces for children and adults at Dr Sobti's Dental Care, Rajouri "
           'Garden. Braces start from ₹40,000.',
  'prices': [('Metal braces', 'From ₹40,000'),
             ('Ceramic (tooth-coloured) braces', 'From ₹50,000'),
             ('Self-ligating braces', 'From ₹60,000')],
  'sections': [('Choosing between the three',
                [['Metal braces are the most affordable and the most robust.',
                  'Ceramic braces use tooth-coloured brackets, so they are much less noticeable.',
                  'Self-ligating braces hold the wire with a built-in clip instead of elastic ties.'],
                 'The cost depends on the type of braces and how complex your case is. You get the full cost in '
                 'writing before treatment starts.']),
               ('How long braces take',
                ['Treatment usually takes between 6 months and two and a half years, depending on how much the teeth '
                 'need to move.']),
               ('Children and adults',
                ['Anyone can have orthodontic treatment, from children to adults. For children, an early check '
                 'around age 7 or 8 shows whether the jaws are growing well and whether braces will be needed later. '
                 'See <a href="/kids-dentist-delhi.html">children\'s dentistry</a>. If you would rather not have '
                 'visible braces, <a href="/clear-aligners-cost-delhi.html">clear aligners</a> are another option.']),
               ('When the jaw needs surgery too',
                ["Some bites can't be fixed by moving teeth alone, for example when the lower jaw is set well "
                 'forward or back. Surgical orthodontics combines braces with jaw surgery. It is planned with a CBCT '
                 'scan, and the cost is given after the planning visit.'])],
  'facts': [('Metal', 'From ₹40,000'),
            ('Ceramic', 'From ₹50,000'),
            ('Self-ligating', 'From ₹60,000'),
            ('Types', 'Metal, ceramic, self-ligating'),
            ('For', 'Children and adults'),
            ('Duration', '6 months to 2½ years')],
  'faq': [('How much do braces cost in Delhi?',
           "At Dr Sobti's Dental Care in Rajouri Garden, metal braces start from ₹40,000, ceramic braces from "
           '₹50,000 and self-ligating braces from ₹60,000. The final cost depends on the case.'),
          ('What is the cost of ceramic braces in India?',
           'Ceramic braces cost in India changes from city to city and with the case. At our Rajouri Garden clinic '
           'they start from ₹50,000 for the full treatment.'),
          ('How long do I need to wear braces?',
           'Usually between 6 months and two and a half years, depending on the case.'),
          ('Can adults get braces?', 'Yes. We treat children and adults.')],
  'cta': 'Book a braces consultation'},
 {'slug': 'clear-aligners-cost-delhi.html',
  'wa': 'Clear aligners',
  'name': 'Clear aligners',
  'title': "Invisalign and Clear Aligners Cost in Delhi: from ₹60,000 | Dr Sobti's Dental Care",
  'desc': 'Invisalign and other clear aligners in Rajouri Garden, Delhi. See your new smile on screen after a 3D '
          'scan. Message or call to ask the cost for your case.',
  'label': 'Treatments · Clear aligners',
  'h1': 'Invisalign and clear aligners cost in Delhi',
  'intro': "Nearly invisible, removable aligners from Invisalign and other leading brands at Dr Sobti's Dental Care, "
           'Rajouri Garden. Treatment starts from ₹60,000.',
  'prices': [('Mild cases', 'From ₹60,000'), ('3D scan and smile preview', 'Included')],
  'sections': [('Which aligner brand',
                ['We work with Invisalign and the other main aligner brands, including Illusion, Flash and 32 Watts. '
                 'Dr Parul will suggest the one that fits your teeth and budget.']),
               ('See the result before you start',
                ['Your teeth are scanned in 3D, and you can see a preview of how your smile will look after '
                 'treatment before you decide anything.']),
               ('What changes the price',
                ['The price mainly depends on how much your teeth need to move and so how many aligners you need. '
                 'Mild crowding or small gaps cost less; bite problems and severe crowding cost more. Treatment time '
                 'also depends on the case.',
                 'If you prefer fixed braces, see <a href="/braces-cost-delhi.html">braces cost in Delhi</a>.'])],
  'facts': [('Mild cases', 'From ₹60,000'),
            ('Brands', 'Invisalign and others'),
            ('Smile preview', 'After your 3D scan')],
  'faq': [('How much does Invisalign cost in Delhi?',
           'It depends on the brand and how much the teeth need to move. Send us a WhatsApp message on 80767 77307 '
           'or call 87449 85976. The front desk will check with the doctor and tell you the cost for your case.'),
          ('What is the cost of invisible braces in Delhi?',
           'Invisible braces, or clear aligners, start from ₹60,000 for mild cases.'),
          ('Is clear aligners cost in India lower than Invisalign?',
           'Often, yes. Several Indian aligner brands cost less than Invisalign for the same kind of case. Dr Parul '
           'will show you the options side by side after your scan, so you can compare.'),
          ('Can I see my new smile before starting?',
           'Yes. After a 3D scan you can see a preview of your smile at the end of treatment.'),
          ('How long does aligner treatment take?',
           'It depends on the case. Dr Parul will tell you the expected time after your scan.')],
  'cta': 'Book an aligner consultation'},
 {'slug': 'root-canal-cost-delhi.html',
  'wa': 'Root canal',
  'name': 'Root canal treatment',
  'title': "Root Canal Treatment Cost in Delhi: from ₹6,000 | Dr Sobti's Dental Care",
  'desc': 'Root canal (RCT) cost in Delhi: front tooth from ₹6,000, back tooth from ₹8,000. Single-sitting RCT with '
          'rotary files, a dental microscope and laser in Rajouri Garden.',
  'label': 'Treatments · Root canal',
  'h1': 'Root canal treatment cost in Delhi',
  'intro': "Root canal treatment under a dental microscope, with rotary instruments and laser, at Dr Sobti's Dental "
           'Care, Rajouri Garden. RCT starts from ₹6,000.',
  'prices': [('Root canal, front tooth', 'From ₹6,000'),
             ('Root canal, back tooth (molar)', 'From ₹8,000'),
             ('Crown after RCT', 'Separate. Zirconia from ₹8,000, E-max from ₹10,000')],
  'sections': [('Single-sitting root canal',
                ['Many root canals can be finished in a single sitting. Whether yours can depends on the tooth and '
                 'the infection, and you will know after the X-ray.']),
               ('Microscope, rotary and laser',
                [['A dental microscope shows the tiny canals inside the tooth, so none are missed.',
                  'Rotary instruments clean and shape the canals faster and more evenly than hand files.',
                  'Laser helps disinfect the canals.']]),
               ('Do you need a cap after root canal?',
                ['A back tooth usually needs a crown after root canal, because the tooth becomes more brittle. The '
                 'crown is separate from the root canal. See <a href="/dental-crown-cost-delhi.html">crowns</a>.'])],
  'facts': [('Front tooth', 'From ₹6,000'),
            ('Back tooth', 'From ₹8,000'),
            ('Single sitting', 'Where suitable'),
            ('Technology', 'Microscope, rotary, laser'),
            ('Crown after RCT', 'Made in our own lab')],
  'faq': [('How much does root canal treatment cost in Delhi?',
           'It depends on the tooth, since a back tooth has more canals than a front one, and the crown is separate. '
           'Send us a WhatsApp message on 80767 77307 or call 87449 85976. The front desk will check with the doctor '
           'and tell you the cost for your case.'),
          ('What is RCT cost in Delhi for a back tooth?',
           'A molar has more canals, so it takes longer. Here RCT on a back tooth starts from ₹8,000, and the crown '
           'is extra.'),
          ('Is single-sitting root canal possible?',
           'Yes, in many cases. It depends on the tooth and the infection, and the cost depends on the case.'),
          ('How much does a redo root canal cost?',
           'A redo costs more than a first root canal, because the old filling has to come out first. Send us a '
           'WhatsApp message on 80767 77307 or call 87449 85976. The front desk will check with the doctor and tell '
           'you the cost for your case.'),
          ('Is the cap included in the RCT price?',
           'No, the crown is separate. Zirconia crowns start from ₹8,000 and E-max crowns from ₹10,000 per tooth.')],
  'cta': 'Book a check-up'},
 {'slug': 'teeth-cleaning-cost-delhi.html',
  'wa': 'Cleaning and air polishing',
  'name': 'Teeth cleaning',
  'title': "Teeth Cleaning and Air Polishing Cost in Delhi: from ₹3,500 | Dr Sobti's Dental Care",
  'desc': "Scaling, polishing, air polishing and deep cleaning at Dr Sobti's Dental Care, Rajouri Garden, Delhi. "
          'Gentle, no-paste stain removal. Message or call to ask the cost.',
  'label': 'Treatments · Cleaning and scaling',
  'h1': 'Teeth cleaning, scaling and air polishing cost in Delhi',
  'intro': "Professional scaling, polishing and air polishing at Dr Sobti's Dental Care, Rajouri Garden. A cleaning "
           'visit starts from ₹3,500.',
  'prices': [('Scaling and polishing', 'From ₹3,500'), ('Air polishing', 'From ₹3,500')],
  'sections': [('What happens at a cleaning',
                ["Scaling removes the hard tartar that brushing can't, especially along the gum line. Polishing then "
                 'smooths the teeth so plaque sticks less. Air polishing uses a fine powder and water spray to lift '
                 'stains from tea, coffee and tobacco.',
                 'A visit takes between 20 minutes and an hour, depending on how much cleaning is needed.']),
               ('Air polishing',
                ['Air polishing sprays a fine powder in a jet of air and water. It lifts stains and soft plaque from '
                 "places a rubber polishing cup can't reach well: between teeth, around braces, along the gum line "
                 'and around crowns and implants.',
                 ['There is no gritty paste and no scraping, so most people find it more comfortable than a regular '
                  'polish.',
                  'It works well on tea, coffee, paan and smoking stains.',
                  'It is gentle on gums and on crowns, veneers and implants.'],
                 'Air polishing is not bleaching. It brings teeth back to their own natural shade. If you want them '
                 'lighter than that, see <a href="https://drparulssobti.com/teeth-whitening-cost-delhi.html">teeth '
                 'whitening</a>.',
                 'Many patients book an air polishing session every six months along with their check-up.']),
               ('Deep cleaning for gum problems',
                ['If your gums bleed or have pulled away from the teeth, a deep cleaning below the gum line may be '
                 'needed. It is done one quarter of the mouth (quadrant) at a time.'])],
  'facts': [('Scaling', 'From ₹3,500'),
            ('Air polishing', 'From ₹3,500'),
            ('Deep cleaning', 'One quadrant at a time'),
            ('Time', '20 minutes to 1 hour')],
  'faq': [('How much does teeth cleaning cost in Delhi?',
           'It depends on how much tartar and staining there is. Send us a WhatsApp message on 80767 77307 or call '
           '87449 85976. The front desk will check with the doctor and tell you the cost for your case.'),
          ('How much does deep cleaning cost?',
           'Deep cleaning is done one quarter of the mouth at a time, so the cost depends on how many quarters need '
           'it. Send us a WhatsApp message on 80767 77307 or call 87449 85976. The front desk will check with the '
           'doctor and tell you the cost for your case.'),
          ('What is air polishing and is it better than normal cleaning?',
           'Air polishing uses a fine powder with air and water to remove stains and plaque. It reaches between '
           'teeth and around braces better than a polishing cup, and most people find it more comfortable. Hard '
           'tartar still needs scaling first, so the two are often done together.'),
          ('Does air polishing whiten teeth?',
           "It removes surface stains, so teeth look brighter, but it doesn't change their natural shade. That needs "
           'whitening.'),
          ('Does scaling damage the teeth?',
           'No. Scaling removes tartar from the surface of the teeth. Teeth can feel sensitive for a day or two '
           'afterwards, and that settles on its own.'),
          ('How long does a cleaning take?', 'Between 20 minutes and an hour, depending on the case.')],
  'cta': 'Book a cleaning'},
 {'slug': 'kids-dentist-delhi.html',
  'wa': 'Kids dentistry',
  'name': "Children's dentistry",
  'title': "Kids Dentist in Rajouri Garden, Delhi: Gentle Children's Dentistry | Dr Sobti's Dental Care",
  'desc': "Children's dentist in Rajouri Garden, West Delhi: check-ups, fillings, root canal and crowns for milk "
          'teeth, early braces checks and laughing gas for nervous kids. Open 7 days.',
  'label': "Treatments · Children's dentistry",
  'h1': "Children's dentist in Rajouri Garden, Delhi",
  'intro': "Check-ups, fillings, root canals and crowns for milk teeth, and early orthodontic checks, at Dr Sobti's "
           "Dental Care, Rajouri Garden. We go at your child's pace, and parents are welcome in the room.",
  'sections': [('The first visit',
                ['A first visit is mostly about getting comfortable. Your child sits in the chair, tries the water '
                 'spray, counts teeth with the doctor and looks at them on the screen. If there is a cavity, we '
                 'explain what we found to you and plan the treatment for another day, unless it is hurting now.',
                 'Children usually do better in the morning, when they are fresh. The clinic is open 7 days, so a '
                 "Saturday or Sunday visit doesn't mean missing school."]),
               ('Why milk teeth are worth saving',
                ['Milk teeth hold the space for the adult teeth coming up underneath. If one is lost too early, the '
                 'teeth beside it drift and the adult tooth can come in crooked. A decayed milk tooth can also hurt '
                 'and get infected just like an adult tooth.',
                 ['Fillings: tooth-coloured fillings for small and medium cavities.',
                  'Root canal for milk teeth: when decay reaches the nerve, the tooth can often be saved instead of '
                  'pulled out.',
                  'Crowns: a badly broken-down milk tooth gets a cap so it lasts until the adult tooth replaces '
                  'it.']]),
               ('Early braces checks',
                ['An orthodontic check around age 7 or 8 shows whether the jaws are growing in a good direction. '
                 'Some problems, like a narrow upper jaw or a crossbite, are easier to correct while a child is '
                 'still growing. Many children need nothing yet, and we simply check again later. See <a '
                 'href="/braces-cost-delhi.html">braces for children and adults</a>.']),
               ('For nervous children',
                ['Laughing gas (nitrous oxide) is a mild sedative breathed through a small nose mask. Your child '
                 'stays awake and can talk, but feels calm and a bit floaty. It wears off within minutes after the '
                 'mask comes off, so they can go home normally.'])],
  'facts': [('Parents', 'Welcome in the room'),
            ('Laughing gas', 'For nervous children'),
            ('Weekends', 'Open Saturday and Sunday')],
  'faq': [('When should my child first see a dentist?',
           'By their first birthday, or within six months of the first tooth coming in. An early visit is short and '
           'easy, and it means problems are caught while they are small.'),
          ('Do milk teeth really need a root canal?',
           'Sometimes, yes. A milk tooth that falls out years too early can cause crowding of the adult teeth. If '
           'the nerve is infected but the tooth can be saved, a root canal for milk teeth keeps it in place until it '
           'falls out naturally.'),
          ('Is laughing gas safe for children?',
           'Nitrous oxide is a mild sedative widely used for children. Your child stays awake, and the effect wears '
           'off within minutes after the mask comes off.'),
          ('At what age can children get braces?',
           'Most full braces start once the adult teeth are in, usually between 11 and 14. An earlier check at 7 or '
           '8 tells you whether any treatment is needed sooner.'),
          ("Can I book my child's visit on a Sunday?",
           'Yes. Our Rajouri Garden clinic is open 7 days, 10 am to 7 pm. WhatsApp 80767 77307 to book.')],
  'cta': "Book your child's check-up"},
 {'slug': 'wisdom-tooth-removal-cost-delhi.html',
  'wa': 'Wisdom tooth',
  'name': 'Wisdom tooth removal',
  'title': "Wisdom Tooth Removal Cost in Delhi: Impacted Wisdom Tooth Surgery | Dr Sobti's Dental Care",
  'desc': 'Wisdom tooth extraction in Rajouri Garden, West Delhi: CBCT scan before surgery, local anaesthetic, '
          'laughing gas if you are nervous. Simple and impacted wisdom teeth.',
  'label': 'Treatments · Wisdom tooth removal',
  'h1': 'Wisdom tooth removal in Delhi',
  'intro': "Simple and surgical removal of wisdom teeth, including impacted ones, at Dr Sobti's Dental Care, Rajouri "
           'Garden. Before surgery we check where the tooth sits and how close it is to the nerve on a 3D CBCT scan, '
           'taken in the clinic.',
  'sections': [('Does it need to come out?',
                ['Not every wisdom tooth has to be removed. A healthy one that has come up straight and can be '
                 'cleaned is fine to keep. It is usually better out if:',
                 ['it keeps getting swollen and painful, or the gum over it gets infected;',
                  'food packs behind it and the tooth in front is starting to decay;',
                  'it is growing sideways into the next tooth;',
                  'it is decayed and too far back to fill well.']]),
               ('Why we scan first',
                ['Lower wisdom teeth often sit close to the nerve that gives feeling to the lip and chin. A normal '
                 "X-ray is flat, so it can't show how close. A CBCT scan shows the tooth and the nerve in 3D, and "
                 'the surgery is planned around it. The scanner is in our clinic, so this is done in the same '
                 'visit.']),
               ('On the day',
                ['The area is numbed with a local anaesthetic, so you feel pressure but not pain. If you are '
                 'nervous, laughing gas helps you relax while you stay awake. An erupted wisdom tooth often comes '
                 'out in a few minutes. An impacted one needs a small cut in the gum, and the tooth may be taken out '
                 'in pieces so less bone is removed. Fine surgical work is done under magnification.']),
               ('Healing at home',
                [['Some swelling for two to three days is normal. A cold pack on the cheek helps on the first day.',
                  'Eat soft, cool food for the first day or two and chew on the other side.',
                  "Don't smoke, spit hard or use a straw for a few days, so the clot stays in place.",
                  'Most people are back at work in a day or two. Stitches, if any, come out after about a week.'],
                 'If anything worries you while it heals, WhatsApp us on 80767 77307.'])],
  'facts': [('Scan', 'CBCT in the clinic'),
            ('Comfort', 'Local anaesthetic, laughing gas if needed'),
            ('Back to work', 'Usually in 1 to 2 days')],
  'faq': [('How much does wisdom tooth removal cost in Delhi?',
           'It depends on whether the tooth has come up or is impacted in the bone. Send us a WhatsApp message on '
           '80767 77307 or call 87449 85976. The front desk will check with the doctor and tell you the cost for '
           'your case.'),
          ('Does wisdom tooth removal hurt?',
           'Not during the procedure, because the area is numb. Afterwards it is sore for a few days, and normal '
           'painkillers usually manage it. Laughing gas is available if you are anxious.'),
          ('Should all four wisdom teeth be removed?',
           'Only the ones causing trouble or likely to. A healthy wisdom tooth that has come up straight can stay.'),
          ('Why do I need a CBCT scan for a wisdom tooth?',
           'Lower wisdom teeth are often close to a nerve. The 3D scan shows exactly how close, so the surgery can '
           'be planned safely.'),
          ('How long does it take to heal?',
           'Swelling settles in two to three days and most people go back to work in a day or two. The gum fully '
           'heals over a few weeks.')],
  'cta': 'Book a wisdom tooth check'}]

# Videos per page (ids from videos_data.py)
GENERAL_VIDEOS = {
    "dental-crown-cost-delhi.html": ["2_e0jS8wVsg", "fvKcdFYR3R8"],
    "root-canal-cost-delhi.html": ["kPXjCugNphI", "K6o1xrWnsJ4"],
    "teeth-cleaning-cost-delhi.html": ["Q4XgYfekrpw", "Vu4W2Kl_Mvs"],
    "kids-dentist-delhi.html": ["HMKI76NpUCw", "K6o1xrWnsJ4", "4pk7Kov41sQ", "kQDuNdLutes"],
    "wisdom-tooth-removal-cost-delhi.html": ["a3YGzvm1YsU", "kQDuNdLutes"],
}
