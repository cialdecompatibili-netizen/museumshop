# -*- coding: utf-8 -*-
"""GUIDA-SVILUPPO: crea le categorie dello SHOP (reparti piatti, un solo livello) IT+EN.
Uso: python automation/crea_categorie_shop.py   poi   python automation/allinea_hash.py en
Scrive: _data/catalogo.json (categorie, con tr.en), _data/shop-categorie.json, _negozio/categoria-<id>.md (IT),
en/negozio/categoria/<id-en>.md (EN). Toglie la categoria e il prodotto di esempio del template.
JSON in UTF-8 senza BOM, ensure_ascii=False (docs/ERRORI_NOTI.md punto 23). Idempotente: riesegue senza duplicare."""
import json, os, re, unicodedata
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONA = "\U0001F3F7"  # etichetta, come nel sito di partenza
# (nome IT, descrizione IT, nome EN, descrizione EN)
C = [
 ("Stampe d'Arte","Riproduzioni su carta fine art dei grandi capolavori, pronte per essere incorniciate.","Art Prints","Fine art paper reproductions of the great masterpieces, ready to be framed."),
 ("Poster Digitali","Immagini in alta risoluzione dei grandi capolavori, download immediato, stampabili a casa o in copisteria.","Digital Posters","High-resolution images of the great masterpieces, instant download, printable at home or at a print shop."),
 ("Tazze e Accessori Casa","Tazze, magneti e complementi d'arredo ispirati alle grandi opere, per portare l'arte nella vita quotidiana.","Mugs and Home Accessories","Mugs, magnets and home decor inspired by great works, bringing art into everyday life."),
 ("Cartoline da Collezione","Cartoline artistiche di alta qualità con i capolavori più amati, perfette da collezionare o spedire.","Collectible Postcards","High-quality art postcards with the most loved masterpieces, perfect to collect or send."),
 ("Abbigliamento Arte","T-shirt e capi ispirati ai grandi maestri, per indossare la passione per l'arte ogni giorno.","Art Apparel","T-shirts and clothing inspired by the great masters, to wear your passion for art every day."),
 ("Borse e Tote Bag","Tote bag e borse in tela con stampe iconiche, pratiche per la spesa o come accessorio quotidiano.","Bags and Tote Bags","Canvas tote bags with iconic prints, practical for shopping or as an everyday accessory."),
 ("Gioielli Ispirati all'Arte","Gioielli ed accessori che reinterpretano motivi e dettagli dei grandi capolavori.","Art-Inspired Jewelry","Jewelry and accessories that reinterpret motifs and details of the great masterpieces."),
 ("Cartoleria e Libri","Quaderni, agende e libri d'arte per accompagnare studio, lavoro e creatività quotidiana.","Stationery and Books","Notebooks, planners and art books to accompany study, work and everyday creativity."),
 ("Antico Egitto","Piramidi, faraoni e geroglifici: prodotti ispirati a una delle civiltà più iconiche della storia.","Ancient Egypt","Pyramids, pharaohs and hieroglyphs: products inspired by one of history's most iconic civilizations."),
 ("Antica Grecia","Ceramiche, statue classiche e miti degli dei greci, per chi ama le origini dell'arte occidentale.","Ancient Greece","Ceramics, classical statues and myths of the Greek gods, for lovers of the origins of Western art."),
 ("Rinascimento","Leonardo, Michelangelo, Raffaello: i capolavori del Rinascimento italiano su ogni tipo di prodotto.","Renaissance","Leonardo, Michelangelo, Raphael: the masterpieces of the Italian Renaissance on every kind of product."),
 ("Mesopotamia e Vicino Oriente Antico","Sumeri, Babilonesi e Assiri: la culla della civiltà tra scrittura cuneiforme e antichi imperi.","Mesopotamia and the Ancient Near East","Sumerians, Babylonians and Assyrians: the cradle of civilization, between cuneiform writing and ancient empires."),
 ("Antica Roma","Mosaici, busti e affreschi dell'Impero Romano, per chi ama la grandezza della classicità latina.","Ancient Rome","Mosaics, busts and frescoes of the Roman Empire, for lovers of the grandeur of Latin antiquity."),
 ("Medioevo","Arte bizantina, gotico e miniature: l'epoca di cattedrali, codici miniati e simbolismo sacro.","Middle Ages","Byzantine art, Gothic and miniatures: the age of cathedrals, illuminated manuscripts and sacred symbolism."),
 ("Arte Precolombiana","Maya, Aztechi e Inca: maschere, dei e simboli delle grandi civiltà dell'America precolombiana.","Pre-Columbian Art","Maya, Aztecs and Incas: masks, gods and symbols of the great civilizations of pre-Columbian America."),
 ("Arte Islamica","Calligrafia, geometrie e arabeschi: la raffinatezza decorativa del mondo islamico classico.","Islamic Art","Calligraphy, geometry and arabesques: the decorative refinement of the classical Islamic world."),
 ("Arte Asiatica","Cina, Giappone e Sud-Est asiatico: porcellane, stampe e sculture di millenni di civiltà orientali.","Asian Art","China, Japan and Southeast Asia: porcelain, prints and sculptures from millennia of Eastern civilizations."),
 ("Arte Africana e Oceaniana","Maschere tribali, sculture rituali e arte primitiva: l'energia espressiva di Africa e Oceania.","African and Oceanic Art","Tribal masks, ritual sculptures and primitive art: the expressive energy of Africa and Oceania."),
 ("Barocco","Caravaggio, Bernini, Rubens: teatralità, luce drammatica e movimento nell'arte del Seicento.","Baroque","Caravaggio, Bernini, Rubens: theatricality, dramatic light and movement in 17th-century art."),
 ("Impressionismo","Monet, Degas, Renoir: luce, colore e attimo fuggente nella rivoluzione pittorica di fine Ottocento.","Impressionism","Monet, Degas, Renoir: light, colour and the fleeting moment in the painting revolution of the late 19th century."),
 ("Preistoria","Arte rupestre, megaliti e le prime forme d'espressione dell'umanità, da Lascaux a Stonehenge.","Prehistory","Cave art, megaliths and humanity's first forms of expression, from Lascaux to Stonehenge."),
 ("Romanticismo e Neoclassicismo","Goya, David, Delacroix: passione, natura e ideali classici tra Settecento e Ottocento.","Romanticism and Neoclassicism","Goya, David, Delacroix: passion, nature and classical ideals between the 18th and 19th centuries."),
 ("Arte Moderna del Novecento","Cubismo, surrealismo, espressionismo: Klimt, Munch e la rivoluzione delle avanguardie del XX secolo.","20th-Century Modern Art","Cubism, surrealism, expressionism: Klimt, Munch and the revolution of the 20th-century avant-gardes."),
 ("Arte Contemporanea","Pop art, street art e arte digitale: le espressioni più recenti e provocatorie della creatività umana.","Contemporary Art","Pop art, street art and digital art: the most recent and provocative expressions of human creativity."),
 ("Futurismo","Boccioni, Balla, Depero: velocità, macchine e movimento nell'avanguardia italiana che ha immaginato il futuro cent'anni fa.","Futurism","Boccioni, Balla, Depero: speed, machines and movement in the Italian avant-garde that imagined the future a hundred years ago."),
 ("Fantascienza Retro","Astronavi, robot e viaggi nel tempo con l'estetica pulp e vintage della sci-fi classica, da Ritorno al Futuro alle copertine anni '50-'80.","Retro Sci-Fi","Spaceships, robots and time travel with the pulp and vintage look of classic sci-fi, from Back to the Future to 1950s-80s covers."),
 ("Cyberpunk","Neon, metropoli distopiche e tecnologia estrema: l'immaginario cyberpunk tra Blade Runner e l'estetica hi-tech contemporanea.","Cyberpunk","Neon, dystopian cities and extreme technology: the cyberpunk imagination between Blade Runner and contemporary hi-tech aesthetics."),
]
def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")
def rd(p): return json.load(open(os.path.join(R, p), encoding="utf-8-sig"))
def wj(p, d): open(os.path.join(R, p), "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
def wt(p, t):
    p = os.path.join(R, p); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write(t)
# catalogo: sostituisce le categorie (e toglie il prodotto di esempio)
cat = rd("_data/catalogo.json")
cat["categorie"] = [{"nome": a, "id": slug(a), "icona": ICONA, "descrizione": b,
                     "tr": {"en": {"nome": c, "descrizione": d}}} for a, b, c, d in C]
cat["prodotti"] = [p for p in cat.get("prodotti", []) if p.get("id") != "prodotto-esempio"]
wj("_data/catalogo.json", cat)
wj("_data/shop-categorie.json", [{"nome": a, "slug": slug(a)} for a, _, _, _ in C])
# pagine: via gli esempi, una pagina IT + una EN per categoria
for old in ("_negozio/categoria-esempio.md", "_negozio/prodotto-esempio.md", "en/negozio/categoria/esempio.md", "en/negozio/prodotto-esempio.md"):
    q = os.path.join(R, old)
    if os.path.exists(q): os.remove(q)
for a, b, c, d in C:
    i, e = slug(a), slug(c)
    wt(f"_negozio/categoria-{i}.md", f'---\nlayout: negozio-categoria\ntitle: "{a}"\ncid: {i}\npermalink: /negozio/categoria/{i}/\ndescription: "{b}"\nref: shop-cat-{i}\n---\n')
    wt(f"en/negozio/categoria/{i}.md", f'---\nlayout: negozio-categoria\ntitle: "{c}"\ncid: {i}\npermalink: /en/shop/category/{e}/\ndescription: "{d}"\nlang: en\nlocale: en\nref: shop-cat-{i}\ntr: tradotto\ntr_hash: 0\n---\n')
print("OK", len(C), "categorie shop")
