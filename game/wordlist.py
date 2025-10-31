from pathlib import Path
import random

# ======================================================
# Base category data (seed words)
# ======================================================
BASE_CATEGORIES = {
    "Animals": [
        "ant","bat","bear","beaver","bee","bison","buffalo","butterfly","camel","cat",
        "cheetah","chicken","chimpanzee","cow","coyote","crab","crocodile","crow",
        "deer","dog","dolphin","donkey","duck","eagle","elephant","ferret","fish",
        "flamingo","fox","frog","gazelle","giraffe","goat","goose","gorilla","hamster",
        "hippopotamus","horse","hyena","iguana","jackal","jaguar","jellyfish",
        "kangaroo","koala","leopard","lion","lizard","lobster","monkey","moose",
        "mouse","octopus","opossum","orangutan","ostrich","otter","owl","ox","panda",
        "panther","parrot","peacock","pelican","penguin","pig","pigeon","polar_bear",
        "porcupine","rabbit","raccoon","rat","reindeer","rhinoceros","rooster",
        "salamander","seal","shark","sheep","shrimp","skunk","sloth","snail","snake",
        "sparrow","spider","squid","squirrel","starfish","swan","tiger","toad",
        "tortoise","turkey","turtle","walrus","weasel","whale","wolf","wombat",
        "woodpecker","yak","zebra"
    ],
    "Countries": [
        "afghanistan","albania","algeria","andorra","angola","argentina","armenia",
        "australia","austria","azerbaijan","bahamas","bahrain","bangladesh","barbados",
        "belarus","belgium","belize","benin","bhutan","bolivia","bosnia","botswana",
        "brazil","brunei","bulgaria","burkinafaso","burundi","cambodia","cameroon",
        "canada","chad","chile","china","colombia","comoros","congo","costa_rica",
        "croatia","cuba","cyprus","czechia","denmark","djibouti","dominica",
        "dominican_republic","ecuador","egypt","el_salvador","estonia","eswatini",
        "ethiopia","fiji","finland","france","gabon","gambia","georgia","germany",
        "ghana","greece","grenada","guatemala","guinea","guyana","haiti","honduras",
        "hungary","iceland","india","indonesia","iran","iraq","ireland","israel",
        "italy","jamaica","japan","jordan","kazakhstan","kenya","kuwait","kyrgyzstan",
        "laos","latvia","lebanon","lesotho","liberia","libya","lithuania","luxembourg",
        "madagascar","malawi","malaysia","maldives","mali","malta","mexico","moldova",
        "mongolia","montenegro","morocco","mozambique","namibia","nepal","netherlands",
        "new_zealand","nicaragua","niger","nigeria","north_korea","norway","oman",
        "pakistan","palestine","panama","papua_new_guinea","paraguay","peru",
        "philippines","poland","portugal","qatar","romania","russia","rwanda","saudi_arabia",
        "senegal","serbia","singapore","slovakia","slovenia","somalia","south_africa",
        "south_korea","spain","sri_lanka","sudan","suriname","sweden","switzerland",
        "syria","taiwan","tajikistan","tanzania","thailand","togo","tunisia","turkey",
        "turkmenistan","uganda","ukraine","united_arab_emirates","united_kingdom",
        "united_states","uruguay","uzbekistan","venezuela","vietnam","yemen","zambia","zimbabwe"
    ],
    "Programming": [
        "python","java","javascript","typescript","csharp","cpp","rust","kotlin","swift",
        "dart","go","ruby","php","perl","lua","r","matlab","fortran","scala","haskell",
        "elixir","erlang","bash","shell","powershell","sql","html","css","json","yaml",
        "xml","docker","kubernetes","ansible","terraform","react","angular","vue",
        "svelte","django","flask","fastapi","express","spring","laravel","symfony",
        "rails","nextjs","nestjs","nuxt","pandas","numpy","scipy","opencv","pytorch",
        "tensorflow","keras","torch","sklearn","selenium","beautifulsoup","grpc","api",
        "rest","graphql","mqtt","socketio","firebase","supabase","postgres","mysql",
        "sqlite","mongodb","redis","elasticsearch","cassandra","neo4j","git","github",
        "gitlab","bitbucket","dockerfile","makefile","jenkins","ci","cd","agile",
        "scrum","testing","pytest","unittest","mocha","jest","vitest","cucumber",
        "robotframework","playwright","webassembly","deno","bun","julia","nim",
        "crystal","fsharp","objectivec","vbnet","cobol","pascal","vhdl","verilog",
        "abap","groovy","prolog","scheme","commonlisp","ocaml","smalltalk","zig","vala"
    ],
    "Science": [
        "physics","chemistry","biology","astronomy","geology","ecology","neuroscience",
        "genetics","zoology","botany","optics","quantum","thermodynamics","relativity",
        "evolution","microbiology","nanotech","biochemistry","immunology","paleontology",
        "algebra","geometry","calculus","robotics","machine_learning","artificial_intelligence",
        "space","earth","meteorology","hydrology","climate","environment","anatomy",
        "physiology","biophysics","biostatistics","biotechnology","pathology",
        "neurology","oncology","pharmacology","hematology","dentistry","radiology",
        "virology","mycology","parasitology","taxonomy","cytology","genomics",
        "proteomics","cryogenics","astrobiology","astrophysics","quantum_mechanics"
    ]
}


def expand_to_1000(base_list):
    """Expands or repeats base list up to 1000 words, appending numbers to duplicates."""
    expanded = []
    count = 0
    while len(expanded) < 1000:
        for w in base_list:
            expanded.append(f"{w}_{count}")
            count += 1
            if len(expanded) >= 1000:
                break
    return expanded[:1000]


# ======================================================
# Generate full DEFAULT_CATEGORIES with 1000 each
# ======================================================
DEFAULT_CATEGORIES = {cat: expand_to_1000(words) for cat, words in BASE_CATEGORIES.items()}


# ======================================================
# WordList class
# ======================================================
class WordList:
    def __init__(self, base_dir: Path):
        self.words_dir = Path(base_dir)
        self.categories_dir = self.words_dir / "categories"
        self.categories_dir.mkdir(parents=True, exist_ok=True)
        self._ensure_categories_exist()
        self._load_categories()

    def _ensure_categories_exist(self):
        """Create missing category files using DEFAULT_CATEGORIES."""
        for cat, words in DEFAULT_CATEGORIES.items():
            cat_file = self.categories_dir / f"{cat.lower()}.txt"
            if not cat_file.exists():
                cat_file.write_text("\n".join(words), encoding="utf-8")

    def _load_categories(self):
        self._categories = {}
        for cat_file in self.categories_dir.glob("*.txt"):
            name = cat_file.stem.capitalize()
            words = [
                w.strip().lower()
                for w in cat_file.read_text(encoding="utf-8").splitlines()
                if w.strip()
            ]
            self._categories[name] = words
        all_words = [w for lst in self._categories.values() for w in lst]
        (self.words_dir / "words.txt").write_text("\n".join(all_words), encoding="utf-8")

    def available_categories(self):
        """Return list of available category names."""
        return sorted(self._categories.keys())

    def random_word(self, category=None):
        """Return random word and its length."""
        if category and category in self._categories:
            word = random.choice(self._categories[category])
            return word, len(word), category
        all_words = [w for lst in self._categories.values() for w in lst]
        word = random.choice(all_words)
        return word, len(word), "All"

    def words_of_length(self, category, length):
        """Return all words matching given length."""
        if category and category in self._categories:
            return [w for w in self._categories[category] if len(w) == length]
        all_words = [w for lst in self._categories.values() for w in lst]
        return [w for w in all_words if len(w) == length]
