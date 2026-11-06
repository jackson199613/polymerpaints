# -*- coding: utf-8 -*-
"""GEO-A05 technical white paper. One content source for the web page and the PDF.

Rules: POLYMER figures come only from the verified company data (catalogue, QC table, certificates).
General industry practice is written as general practice ("typically", "many buyers"), never as a POLYMER
guarantee. No survey data, no fixed outdoor lifetimes, Qualicoat scope stated, ISO = management systems,
in-house tests described as internal, epoxy indoor only, no UL / flame-retardant / IATF claims.
"""

WP = {
    'slug': 'powder-coating-specification-guide',
    'title': 'Powder Coating Specification Guide for Importers and Manufacturers',
    'short': 'Powder coating specification guide',
    'subtitle': 'How to choose the system, specify colour and effect, approve a reference panel and keep every batch true to it.',
    'edition': 'Edition 1 · November 2026',
    'date': '2026-11-05',
    'pages_note': 'Technical white paper',
    'desc': 'Free technical white paper: how to specify powder coatings by environment, cure, colour, gloss and effect, approve reference panels, read certificates and move from sample to bulk.',
    'pdf': '/assets/docs/polymer-powder-coating-specification-guide-2026-11.pdf',
    'audience': ['Purchasing managers at importers and distributors', 'Product and QC managers at metal-part manufacturers', 'Coating applicators and job shops', 'Specifiers for aluminium profiles and facades'],
    'summary': [
        'Choose the resin system from the service environment first: polyester for outdoor or UV exposure, hybrid for indoor decorative parts, epoxy for indoor functional parts. Price comes after.',
        'A colour code is not a specification. Specify colour together with gloss band, effect, film thickness and cure, and approve all of them on a physical panel.',
        'Make the approved panel a numbered version. Every batch is compared with that version, and any change becomes a new version instead of a silent drift.',
        'Read every certificate for its scope: a Qualicoat approval covers the named system, ISO 9001 and ISO 14001 cover management systems, and a test report covers the sample tested.',
        'Trial the powder on your own line before bulk supply. Pretreatment, oven profile and reclaim change the result more often than the powder does.',
    ],
    'sections': [
        {'id': 'environment', 'title': 'Which resin system does the service environment call for?',
         'paras': [
             'Thermosetting powder coatings for metal are made from three main resin families: polyester, epoxy and epoxy-polyester hybrid. All three can be produced in the same RAL colours, gloss bands and textures, so on a sample shelf they can look identical. They separate later, when the part meets sunlight, chemicals, heat or mechanical wear.',
             'The first specification decision is therefore the environment, not the price or the colour. Ask where the part will be used for most of its life, whether it will see direct sunlight or UV through glass, and whether it will be cleaned with chemicals or handled heavily. A product range that mixes indoor and outdoor items is usually safer on polyester for the outdoor parts than on one powder for everything.',
         ],
         'table': [('', 'Polyester', 'Epoxy-polyester hybrid', 'Epoxy'),
                   ('Service environment', 'Outdoor, UV-exposed', 'Indoor, decorative', 'Indoor, functional'),
                   ('Main strengths', 'Weather and UV resistance, edge coverage, impact resistance', 'Smooth flow, high gloss, good mechanical properties, better resistance to yellowing than epoxy', 'Adhesion, hardness, chemical resistance, electrical insulation'),
                   ('Main limits', 'Lower chemical resistance than epoxy', 'Not for direct outdoor use', 'Chalks and changes colour under UV; indoor only'),
                   ('Typical parts', 'Aluminium profiles, outdoor furniture and lighting, AC housings, agricultural machinery', 'Appliances, steel furniture, shelving, indoor cabinets, light fittings', 'Safes, security doors, instrument housings, fitness and indoor equipment')],
         'note': 'Epoxy powder coatings are not a substitute for fusion-bonded epoxy (FBE) or three-layer pipeline systems, and none of the three families should be specified as a heavy-duty anticorrosion system without a separate engineering review.'},

        {'id': 'cure', 'title': 'Standard cure or low cure: what changes on the line?',
         'paras': [
             'Each of the three systems can be supplied in a standard-cure and a low-cure grade. Cure is defined by the metal temperature and the time the part spends at that temperature, not by the oven set point. Thick castings, heavy frames and mixed loads reach temperature later than thin sheet, so the slowest part on the hanger decides the real cure.',
             'Low-cure grades help with heavy parts, heat-sensitive assemblies and energy saving. They are more reactive, so they are more sensitive to storage temperature and need a measured oven profile before the switch. Always take the cure window from the technical data sheet of the specific product and confirm it with an oven temperature logger on your own line.',
         ],
         'bullets': ['Log the metal temperature on the heaviest and lightest parts of a typical load.',
                     'Compare the logged curve with the cure window on the TDS, not with the oven display.',
                     'Check cure on trial parts (for example a solvent rub test and the mechanical tests in section 6) before bulk production.',
                     'Store low-cure powder in the coolest part of the warehouse and use it in stock rotation.']},

        {'id': 'appearance', 'title': 'How do you specify colour, gloss and effect so they can be repeated?',
         'paras': [
             'A colour code such as RAL 7016 names a colour, but it does not fix gloss, texture or how the colour looks after cure on your substrate. Two powders that both match RAL 7016 can look different side by side. A repeatable specification names the colour, the gloss band, the effect and the film thickness, and links them to a physical reference.',
             'Gloss is measured with a 60° gloss meter. Effects change both the look and the measured gloss, so textured and metallic finishes are approved visually against the reference panel as well as by measurement. Metallic effects also change with viewing angle and light, which is why they should never be approved from a printed card or a photograph.',
         ],
         'table': [('Element', 'What to specify', 'Notes'),
                   ('Colour', 'RAL, Pantone or customer sample, plus the reference panel', 'Approve under agreed light (for example D65 in a light box) and state the colour tolerance'),
                   ('Gloss band', 'High gloss ≥90, satin and matt 11–80, dead matt ≤10 (60° gloss units)', 'State a target and an acceptable range within the band'),
                   ('Effect', 'Smooth, sand, fine texture, wrinkle, vein, hammer tone, pattern, metallic, transparent or translucent, fluorescent', 'Texture depends on film thickness and oven profile as much as on the powder'),
                   ('Metallic', 'Bonded or dry-blend, flake colour and size, viewing reference', 'Bonded metallics keep the effect more consistent through spraying and reclaim'),
                   ('Film thickness', 'Target range in µm for the coated face', 'Texture, colour and hiding all change with thickness')],
         'note': 'Many buyers agree a colour tolerance as a colour difference (ΔE) against the approved panel, measured with a spectrophotometer. Agree the value, the instrument geometry and the light source with the supplier before the first order; a number without those conditions cannot be checked.'},

        {'id': 'reference-panel', 'title': 'Why should the approved panel become a numbered version?',
         'paras': [
             'Batch-to-batch differences rarely come from one large error. They come from small, unrecorded changes: a different reference, a new part geometry, a change of oven or film thickness, a new raw material. The most reliable control is to treat the approved panel as a version with its own record, and to compare every batch with that version before it is packed.',
             'When something must change — a new colour, a new part, a different line condition — it becomes a new version with a new approval, rather than a quiet adjustment to the old one. Keep one physical panel at the supplier and one at the line, stored away from light and heat.',
         ],
         'table': [('Record on the approved version', 'Why it matters'),
                   ('Version number and approval date', 'Lets both sides refer to the same reference in every order'),
                   ('Resin system and cure grade', 'Prevents an indoor powder being supplied for an outdoor part'),
                   ('Colour reference and measured values', 'Gives a numerical check alongside the visual one'),
                   ('Gloss target and range', 'Gloss drift is one of the most visible differences between batches'),
                   ('Effect description', 'Texture and metallic effects need a written as well as a physical reference'),
                   ('Film thickness and cure used for the panel', 'The same powder looks different at other thicknesses and cures'),
                   ('Substrate and pretreatment', 'Aluminium and steel, and different pretreatments, change appearance and adhesion')]},

        {'id': 'thickness', 'title': 'How much film thickness, and how much powder per square metre?',
         'paras': [
             'Film thickness affects appearance, hiding power, texture and protection. Specify a target range for the significant surfaces of the part and measure it with an electromagnetic (steel) or eddy-current (aluminium) gauge. For architectural aluminium, the coating specification the project follows usually sets a minimum; follow that document rather than a general rule.',
             'Powder consumption can be estimated from the specific gravity of the powder and the film thickness. The theoretical coverage in square metres per kilogram is 1,000 divided by (specific gravity × film thickness in µm). Real consumption is higher because of transfer efficiency, part geometry and whether overspray is reclaimed.',
         ],
         'table': [('Specific gravity (g/cm³)', 'At 60 µm', 'At 70 µm', 'At 80 µm'),
                   ('1.4', '11.9 m²/kg', '10.2 m²/kg', '8.9 m²/kg'),
                   ('1.6', '10.4 m²/kg', '8.9 m²/kg', '7.8 m²/kg'),
                   ('1.8', '9.3 m²/kg', '7.9 m²/kg', '6.9 m²/kg')],
         'note': 'Theoretical coverage at 100% utilisation. Divide by your real utilisation (for example 0.6 without reclaim) to estimate actual consumption. POLYMER polyester powders have a specific gravity of 1.4–1.8 g/cm³; the value for each product is on its TDS.'},

        {'id': 'tests', 'title': 'Which tests should a specification name?',
         'paras': [
             'A specification is only useful if each requirement can be checked. Name the property, the test method and the acceptance level, and say which tests are run on every batch and which only at approval. International standards give common methods; where your market or customer uses a national standard, name that one instead.',
         ],
         'table': [('Property', 'Common method', 'What it tells you'),
                   ('Film thickness', 'ISO 2360 (aluminium), ISO 2178 (steel)', 'Whether the coating is within the approved range'),
                   ('Gloss', 'ISO 2813, 60° geometry', 'Gloss band and drift between batches'),
                   ('Colour', 'Spectrophotometer plus light-box comparison', 'Difference from the approved panel'),
                   ('Adhesion', 'Cross-cut, ISO 2409 (1 mm spacing for thin films)', 'Bond to the pretreated substrate'),
                   ('Flexibility', 'Bend test, ISO 1519', 'Cracking or loss of adhesion when the part is formed'),
                   ('Impact', 'Falling weight, ISO 6272', 'Resistance to knocks in handling and use'),
                   ('Hardness', 'Pencil hardness, ISO 15184', 'Scratch resistance of the cured film'),
                   ('Corrosion', 'Neutral salt spray, ISO 9227', 'Comparative performance of the coating and pretreatment system'),
                   ('Weathering', 'UV accelerated ageing', 'Comparative gloss and colour retention, mainly for polyester')],
         'note': 'Accelerated tests compare systems under laboratory conditions. They do not predict a fixed number of years outdoors, and results depend heavily on pretreatment. The methods above are common references for buyers. POLYMER’s own laboratory checks film thickness, 60° gloss, colour, particle size, cross-cut adhesion, 180° bend, impact, pencil hardness, salt spray and UV accelerated ageing as in-house test conditions; these are not third-party reports.'},

        {'id': 'certificates', 'title': 'How do you read certificates for their scope?',
         'paras': [
             'Certificates are useful only when you know exactly what they cover. Before relying on one, check the holder, the number, the validity dates and the scope written on the certificate itself, and ask for the document rather than a logo on a brochure.',
         ],
         'table': [('Document', 'What it covers', 'What it does not cover'),
                   ('Qualicoat approval (powder)', 'A named powder system, gloss category and class, for architectural aluminium, for the validity period shown', 'Other products or colours in the catalogue, other classes, or extensions not listed on the certificate'),
                   ('ISO 9001', 'The quality management system of the named site and scope', 'Product performance; it is not a product approval'),
                   ('ISO 14001', 'The environmental management system of the named site and scope', 'Environmental claims about specific products'),
                   ('Test report (for example EU RoHS)', 'The sample tested, on the date and by the method in the report', 'Other colours, batches or products unless they are listed')],
         'note': 'As an example of scope: POLYMER’s Qualicoat approval P-2199 covers polyester system PLM100611, Class 1, gloss category 3, valid until 31 December 2026, with no structured-texture or metallic extension. POLYMER’s ISO 9001:2015 and ISO 14001:2015 certificates cover the design, manufacture and sales of thermosetting powder coatings. Its SGS EU RoHS report covers one black powder sample.'},

        {'id': 'sample-to-bulk', 'title': 'How should a project move from sample to bulk supply?',
         'paras': [
             'Most problems in a new supply relationship appear in the first bulk order, when the powder meets the real line. A staged process catches them earlier and costs less than a rejected container.',
         ],
         'steps': [('Describe the part', 'Part, substrate and pretreatment, service environment, target colour and effect, line and oven conditions, expected annual volume.'),
                   ('Match on panels', 'The supplier proposes a system and matches colour, gloss and effect on panels sprayed and cured under stated conditions.'),
                   ('Trial on your line', 'Spray sample powder on real parts with your pretreatment, guns, oven and reclaim. Check appearance and the agreed tests.'),
                   ('Approve the version', 'Approve the panel that came from the trial conditions and record it as a numbered version.'),
                   ('Bulk and repeat orders', 'Every batch is checked against the version before packing; changes go through a new version.')]},

        {'id': 'storage', 'title': 'How should powder be stored, handled and shipped?',
         'paras': [
             'Powder coatings are sensitive to heat and moisture. Warm or humid storage can cause lumps, poor fluidisation and changes in flow and gloss, and low-cure grades are the most sensitive. Plan storage as part of the specification, especially for long sea freight to warm climates.',
         ],
         'bullets': ['Store sealed, in a dry, ventilated place away from heat sources and direct sun; POLYMER’s storage stability check is 6 months below 30 °C.',
                     'Bring cartons to workshop temperature before opening to avoid condensation on the powder.',
                     'Use stock in order of production date, and keep low-cure powder in the coolest area.',
                     'Confirm packing format and transport classification with the supplier before shipment; POLYMER powders ship as non-dangerous goods according to their SDS.',
                     'Tell the supplier the destination port and required documents with the order, not after production.']},

        {'id': 'checklist', 'title': 'What should a complete specification contain?',
         'paras': ['Use this list as the minimum content of a purchase specification or a request for quotation.'],
         'bullets': ['Part description, substrate and pretreatment',
                     'Service environment: outdoor, indoor decorative or indoor functional',
                     'Resin system and cure grade, with the cure window from the TDS',
                     'Colour reference, light source and colour tolerance',
                     'Gloss band, target and range at 60°',
                     'Effect, and for metallics bonded or dry-blend',
                     'Film thickness range on significant surfaces',
                     'Tests, methods and acceptance levels; which are per batch and which at approval',
                     'Required certificates and their scope; required documents (TDS, SDS, test reports)',
                     'Approved version number and where the reference panels are kept',
                     'Order quantity, lead time, packing, storage and destination port']},
    ],
    'about': [
        'POLYMER Powder Coatings is the brand of Fujian Polymer Industry & Trade Co., Ltd., founded in 2019 in Zhangzhou, Fujian, China. The company makes epoxy, polyester and epoxy-polyester hybrid powder coatings in standard-cure and low-cure grades.',
        'Annual capacity is 5,000 t on 8 production lines, with 5 sampling lines and 2 metallic bonding machines. Standard lead time is within 10 days, with complex custom colours and large volumes confirmed per order; the minimum order is 1,000 kg.',
        'Management systems are certified to ISO 9001:2015 and ISO 14001:2015; polyester system PLM100611 holds Qualicoat Class 1 approval P-2199.',
    ],
    'disclaimer': 'This guide gives general technical guidance for buyers and specifiers. It does not replace the technical data sheet and safety data sheet of a specific product, the specification of a project, or trials on your own line. Figures for POLYMER products are taken from POLYMER’s catalogue and certificates as of the edition date.',
}
