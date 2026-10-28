# -*- coding: utf-8 -*-
"""Insights: long-form buyer articles. Facts follow the catalogue and the content red lines
(no fixed outdoor lifetimes, Qualicoat scope stated, in-house tests described as internal)."""

ARTICLES = [
 {
  'slug': 'polyester-vs-epoxy-vs-hybrid-powder-coating',
  'title': 'Polyester vs epoxy vs hybrid powder coating: a buyer’s comparison',
  'short': 'Polyester vs epoxy vs hybrid',
  'desc': 'How polyester, epoxy and epoxy-polyester hybrid powder coatings differ in UV resistance, chemical resistance, appearance and typical parts, and how to choose by environment.',
  'date': '2026-10-28', 'mins': 6, 'img': ('home/gloss-trio', 1536, 1024, 768, 'Three powder-coated panels in dead matt, satin and high gloss'),
  'lead': 'Most powder coating problems in the field start with the wrong chemistry, not the wrong colour. The fastest way to choose is to ask one question first: where will the part live?',
  'sections': [
   ('Start with the environment, not the price', [
     'Thermosetting powder coatings for metal fall into three families that cover most industrial and decorative work: pure polyester, pure epoxy and epoxy-polyester hybrid. They can all be made in the same RAL colours, gloss bands and textures, so on a sample shelf they can look identical. The difference shows up later, when the part meets sunlight, chemicals or heat.',
     'If the part is used outdoors or is exposed to UV through a window, the choice is polyester. If it stays indoors, the choice is between hybrid for decorative parts and epoxy for functional parts that need chemical resistance, hardness or electrical insulation.']),
   ('The three systems side by side', [], [
     ('', 'Polyester', 'Epoxy-polyester hybrid', 'Epoxy'),
     ('Use', 'Outdoor and UV-exposed', 'Indoor, decorative', 'Indoor, functional'),
     ('Strength', 'Weather and UV resistance, good edge coverage, impact resistance', 'Smooth flow, high gloss, good mechanical properties, better heat and light stability than epoxy', 'Adhesion, hardness, chemical resistance, electrical insulation'),
     ('Limitation', 'Lower chemical resistance than epoxy', 'Not for direct outdoor use', 'Chalks and yellows under UV; not for outdoor use'),
     ('Typical parts', 'Aluminium profiles, outdoor furniture and lighting, air-conditioner housings, agricultural machinery', 'Appliances, steel furniture, shelving, indoor cabinets, light fittings', 'Safes, security doors, instrument housings, fitness equipment, indoor equipment'),
   ]),
   ('Why epoxy should stay indoors', [
     'Epoxy resin gives excellent adhesion and chemical resistance, but its aromatic structure absorbs UV. Outdoors the surface chalks and the colour shifts, often within a single season for bright shades. Over-baking or long cure times also push epoxy towards yellow, which matters for whites and pale colours even indoors.',
     'This is why a part that might end up outdoors, or a product range that mixes indoor and outdoor items, is safer on polyester. One powder for everything usually means the wrong powder for some of the parts.']),
   ('Where hybrid fits', [
     'Hybrid combines epoxy and polyester resins. It keeps much of epoxy’s mechanical performance while improving flow, gloss and resistance to yellowing. For appliances, shelving and indoor furniture it is often the most economical way to get a smooth, attractive film. It should not be specified for outdoor use.']),
   ('Standard cure or low cure?', [
     'All three systems can be supplied in standard-cure and low-cure grades. Low-cure grades help with heavy parts, heat-sensitive assemblies or energy saving, but they are more reactive in storage and need a measured metal-temperature profile on your oven. Read our guide on checking cure before you switch.']),
   ('How to specify your choice', [
     'Send the supplier the part, the substrate and pretreatment, where it will be used, the target colour and gloss, and your oven conditions. A good supplier will confirm the system on panels sprayed on your line rather than from a data sheet alone, and will record the approved panel so repeat orders can be checked against it.']),
  ],
  'related': [('Polyester', '/products/polyester/'), ('Hybrid', '/products/hybrid/'), ('Epoxy', '/products/epoxy/'), ('System selector', '/selector/'), ('How to check that powder coating is fully cured', '/how-to/check-powder-coating-cure/')],
 },
 {
  'slug': 'how-to-source-powder-coatings-from-china',
  'title': 'How to source powder coatings from China: a checklist for importers',
  'short': 'Sourcing powder from China',
  'desc': 'A practical checklist for importers and distributors buying powder coatings from China: systems, samples, approved panels, documents, certificates, MOQ, lead time and shipping.',
  'date': '2026-10-28', 'mins': 7, 'img': ('ind/distributors-b', 1536, 1024, 768, 'Colour panels, colour card and powder sample on a desk'),
  'lead': 'Buying powder from a new supplier is easy. Getting the same colour, gloss and behaviour on the tenth order is the real test. This checklist is built around that.',
  'sections': [
   ('1. Define what you are buying', [
     'List the systems you need (polyester, hybrid, epoxy), the colours and effects your customers ask for most, and which ones are outdoor. Separate the standard range from difficult items such as bonded metallics, fine textures or low-cure grades; those are where suppliers differ most.']),
   ('2. Ask for panels, not just a colour card', [
     'A printed card shows a colour; a sprayed panel shows colour, gloss, texture and film behaviour together. Ask for panels matched to your physical reference, sprayed and cured, with the system, gloss and film thickness written on them. Then spray the sample powder on your own line, because pretreatment and ovens change the result.']),
   ('3. Make the approved panel the contract', [
     'Once a panel is approved, the supplier should record it as a version: system, colour, gloss, texture, film thickness and cure. Every batch is then checked against that reference before shipment, and any change — a new colour, part or condition — becomes a new version rather than a silent change. Ask how the supplier does this before the first order.']),
   ('4. Read certificates for their scope', [
     'Certificates are useful only when you know what they cover. A Qualicoat approval applies to the named system and licence, not to every product or colour. ISO 9001 and ISO 14001 certify management systems, not products. Third-party test reports apply to the sample tested. Ask for the certificate itself and check the licence number, validity and scope.']),
   ('5. Collect the documents your market needs', [
     'At minimum: technical data sheets with cure conditions and storage guidance, safety data sheets, and the relevant certificates. If your customers ask for restricted-substance compliance such as EU RoHS, ask which products and colours a report covers, and whether a report for your colour can be arranged.']),
   ('6. Agree MOQ, lead time and replenishment', [
     'Clarify the minimum order per order and per colour, the standard lead time, and which items take longer. A distributor’s first order is usually a mix of fast-moving standard colours and a few effects. Plan replenishment around the supplier’s real lead time plus sea freight, not the best case.']),
   ('7. Plan packing, storage and shipping', [
     'Powder is sensitive to heat and humidity. Confirm the packing format, storage stability and recommended storage temperature, and whether the product is classified as dangerous goods for transport. Tell the supplier your destination port early so documents and freight are prepared with the order.']),
   ('8. Start small, then scale', [
     'A sensible sequence is panels, a line trial, a first order at the supplier’s MOQ, then regular replenishment once results are stable. Exclusive territories are usually discussed after the first repeat orders, not before.']),
  ],
  'related': [('Distributors', '/distributors/'), ('Request a sample', '/request-sample/'), ('Quality & certificates', '/quality/'), ('Downloads', '/downloads/'), ('FAQ', '/faq/')],
 },
 {
  'slug': 'qualicoat-class-1-explained',
  'title': 'Qualicoat Class 1 explained: what it covers and what to ask your supplier',
  'short': 'Qualicoat Class 1 explained',
  'desc': 'What a Qualicoat Class 1 approval means for architectural aluminium, how to read a powder supplier’s certificate, and the questions to ask before you specify.',
  'date': '2026-10-28', 'mins': 5, 'img': ('ind/aluminium-a', 1024, 683, 600, 'Powder-coated aluminium facade fins'),
  'lead': 'Many architectural projects ask for “Qualicoat powder”. The approval is real and valuable — but it is granted to specific powder systems, so the details on the certificate matter.',
  'sections': [
   ('What Qualicoat is', [
     'Qualicoat is a quality label for liquid and powder coatings on aluminium used in architecture. For powder manufacturers it approves specific powder systems after laboratory testing, and the approval must be renewed. Applicators and extruders hold their own Qualicoat licences for their coating lines.']),
   ('What “Class 1” refers to', [
     'Qualicoat classifies powder systems by durability. Class 1 is the standard architectural class used for most window, door and facade projects. Higher classes cover more demanding durability requirements and are approved separately. A supplier with a Class 1 approval should not be described as holding a higher class unless it has that approval too.']),
   ('How to read a supplier’s certificate', [
     'Check four things: the approval number, the powder system named on the certificate, the gloss category, and the validity date. Also check any extensions or exclusions — for example whether structured textures or metallic finishes are included. The approval covers the named system, not every product or colour in the supplier’s catalogue.',
     'For example, POLYMER’s polyester system PLM100611 holds Qualicoat Class 1 approval P-2199, gloss category 3, valid until 31 December 2026; it has no structured-texture or metallic extension.']),
   ('Questions to ask before you specify', [
     'Which product codes belong to the approved system? Are the colour and gloss you need within it? Is the certificate valid for the duration of your project? Can the supplier provide the certificate itself for your project file? And does your applicator’s own Qualicoat licence cover the line that will coat the profiles?']),
   ('When Qualicoat is not required', [
     'Outdoor furniture, lighting, machinery and many industrial parts need weather-resistant polyester but not necessarily a Qualicoat label. In those cases the decision is about performance on your parts, which panels and line trials confirm.']),
  ],
  'related': [('Architectural aluminium', '/industries/architectural-aluminium/'), ('Polyester', '/products/polyester/'), ('Quality & certificates', '/quality/'), ('FAQ: Qualicoat', '/faq/#what-qualicoat-class-1-covers')],
 },
 {
  'slug': 'bonded-vs-dry-blend-metallic-powder',
  'title': 'Bonded vs dry-blend metallic powder coatings: why it matters on the line',
  'short': 'Bonded vs dry-blend metallics',
  'desc': 'How bonded and dry-blend metallic powder coatings differ, why bonding reduces separation during spraying and reclaim, and how to specify metallic effects.',
  'date': '2026-10-28', 'mins': 5, 'img': ('finish/metallic', 800, 800, 400, 'Bonded metallic powder coating, macro'),
  'lead': 'Metallic and pearlescent effects are among the most attractive powder finishes — and among the hardest to keep consistent. The way the effect pigment is combined with the powder makes most of the difference.',
  'sections': [
   ('What makes a metallic finish', [
     'The effect comes from flake pigments — aluminium, mica or similar — that reflect light. In liquid paint the flakes float and orient in the wet film. In powder, the flakes have to travel through the spray gun, the booth and the reclaim system alongside the powder particles, and they do not always behave the same way.']),
   ('Dry-blend: simple but sensitive', [
     'In a dry-blend the flakes are mixed with the finished base powder. It is quick to produce, but the flakes and the powder particles charge and fly differently. The result can be uneven appearance between parts, differences between first-pass and reclaimed powder, and a gradual change in effect as the reclaim ratio builds up.']),
   ('Bonded: flakes attached to the particles', [
     'In bonded metallic powder the flakes are attached to the powder particles under controlled heat and mixing. Because they move together, the effect stays more consistent from part to part and through reclaim. POLYMER uses two dedicated bonding machines for metallic orders.']),
   ('Specifying a metallic effect', [
     'Describe the target look with a physical reference part or panel rather than a colour code alone, because viewing angle and light change metallics dramatically. Tell the supplier your spray equipment, whether you reclaim, and the parts’ geometry. Approve the effect on panels sprayed under your conditions and keep that panel as the reference.']),
   ('Outdoor metallics', [
     'For outdoor use, metallic effects should be built on a weather-resistant polyester. Check whether a project that requires a Qualicoat label also needs a metallic extension on the certificate.']),
  ],
  'related': [('Colours & finishes', '/finishes/#metallic'), ('FAQ: bonded metallic', '/faq/#what-is-bonded-metallic-powder'), ('Request a sample', '/request-sample/?finish=Metallic')],
 },
 {
  'slug': 'sand-wrinkle-hammer-texture-powder-coatings',
  'title': 'Sand, wrinkle or hammer tone? Choosing a textured powder coating',
  'short': 'Choosing a textured finish',
  'desc': 'Compare sand texture, wrinkle, vein, fine texture and hammer tone powder coatings: how they look, where they are used and how to keep texture consistent.',
  'date': '2026-10-28', 'mins': 5, 'img': ('finish/hammer', 800, 800, 400, 'Hammer tone powder coating, macro'),
  'lead': 'Textured powders hide small substrate defects, resist fingerprints and give parts a more robust feel. Each texture also has its own sensitivities on the line.',
  'sections': [
   ('The main textures', [], [
     ('', 'Look', 'Typical use'),
     ('Sand texture', 'Fine, even grain like fine sandpaper', 'Electrical cabinets, enclosures, office furniture'),
     ('Fine texture', 'Very dense micro-texture, soft-touch matt', 'Furniture, housings, consumer products'),
     ('Wrinkle', 'Continuous soft ridges, like crinkled leather', 'Equipment, tools, instrument cases'),
     ('Vein', 'Irregular network of raised veins over a base tone', 'Decorative metal, hardware'),
     ('Hammer tone', 'Shallow dimples with a metallic highlight', 'Machinery, tools, decorative parts'),
   ]),
   ('Why textures vary between batches and lines', [
     'Texture depends on film thickness, oven profile and spraying conditions as much as on the powder. Thicker films usually give coarser texture; faster heat-up can change wrinkle and vein patterns; reclaimed powder can shift texture slightly. A texture approved at one film thickness may look different at another.']),
   ('How to keep texture consistent', [
     'Approve the texture on a panel sprayed at your normal film thickness and cure, and record both with the approved version. Keep a physical reference at the line. Control the reclaim ratio, and check new batches against the reference panel before full production. Our guide on consistent textures goes step by step.']),
   ('Textures and outdoor use', [
     'Any texture can be produced on a weather-resistant polyester for outdoor parts. Note that Qualicoat approvals may exclude structured textures unless the certificate includes that extension.']),
  ],
  'related': [('Colours & finishes', '/finishes/'), ('How to get consistent textures', '/how-to/consistent-texture-finishes/'), ('Request a sample', '/request-sample/?finish=Sand%20texture')],
 },
]
