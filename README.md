
 Několik (keltských) týmů je tvořeny čtyřmi agenty - druidy, nazvěme je Kněz, Dlouhý, Široký a Bystrozraký. Tyto klany působí na hrací ploše obecně libovolných rozměrů (které pro tento rok budou ve skutečnosti vždy 55x55). Na této ploše mají možnost získávat suroviny, které posléze donášejí do sídla (depotu). Umístění sídel je pro všechny týmy stejné, ale každý klan vytváří svoji kolekci surovin zvlášť. Mezi suroviny se počítá zlato, dřevo, kámen a voda. V sidle se nachází několik kněžích, jeden pro každý klan. Tito mohou ze surovin vyrábět předměty, které mají nějakou hodnotu, která je vyjádřena v jednotkách nějaké místní měny. Hodnota se liší podle toho, kolik surovin je k jejich výrobě potřeba. Knězi znají postupy pro výroby jen několika předmětů, a v tomto zadání to bude jeden až šest postupů, při kterých jsou třeba vždy dvě suroviny. Tyto suroviny mohou být stejného druhu, ale mohou se také lišit. Za takový předmět obdrží klan obnos v hodnotě dvě jednotky druidí měny. Každý tým ale může svému knězi pomoci nalézt nové postupy a to tím, že do sídla dopraví nějaké pergameny, které se na hrací ploše nachází. Poté může kněz přečíst soubor tří až pěti pergamenů, čímž nalezne postup pro výrobu předmětů ze tří až pěti surovin. Může se ale stát, že zjistí postup, který již zná a který nalezl dříve a pak má smůlu. Co je ale přínosné je to, že za předmět vyrobený ze tří surovin získá obnos v hodnotě čtyř, za předmět ze čtyř surovin obnos v hodnotě šesti a za předmět z pěti surovin obnos v hodnotě devíti jednotek měny. Takto může snáze porazit soupeře, druhého Druida, což se mu podaří, pokud první získá obnos v hodnotě sto* jednotek měny, nebo obnos, který aktuálně převyšuje obnos soupeře o dvacet* těchto jednotek. Co mají za schopnosti pěšáci z týmu a jak se liší? Inu Dlouhý dokáže během jednoho kola hry absolvovat bez bot tři kroky, s botami kroků šest. Jeho přítel Bystrozraký udělá za kolo kroky dva a Široký jen jeden krok. Bystrozraký ale dál dohlédne. Bez brýlí do okolí tří políček a s brýlemi dokonce šest políček daleko vidí. To ostatní dva vždy jen jedno políčko kolem vnímají. A co se týče síly, Bystrozraký unese jen jednu surovinu nebo pergamen, dlouhý dvě, ale zato široký hned čtyři, s rukavicemi dokonce osm surovin. Boty, brýle a rukavice se také nachází na hrací ploše a může je zvednout vždy jen ten, komu pomohou. Jak je to se surovinami a ostatními předměty na ploše. Rukavice, boty, brýle, pergameny a zlato, ty jsou na ploše rozmístěny náhodně a agent na políčko s nimi může vstoupit a surovinu zvednout. Stejně tak toto platí pro dřevo, resp. stromy, ale ty jsou na mapě dvakrát uskupeny jako les, takže agent může předpokládat, že kde je jeden strom, může se nacházet stromů víc. Problém může agentům činit to, že na jednom políčku můžou být zároveň dřevo, pergamen a zlato, nebo nějaká dvojice těchto surovin. Pokud agent vstoupí na políčko a provádí akci zvednutí, zvedá suroviny v tomto pořadí, tj. potřebuje provést tři akce ‘pick’, aby zvedl i zlato. Skála, tedy kámen, se nachází v blocích a agent nemůže na políčko se skálou vstoupit. Může ale kámen vytěžit, pokud se nachází v jeho čtyřokolí (S/J/V/Z), pak akcí ‘dig’ s uvedením směru může kámen získat. Co se týče vody, ta může být zrádná. Pokud se agent drží při břehu, to znamená, že některé políčko v jeho osmiokolí je pevnina, neutopí se a může nabírat vodu, kterou Druid může potřebovat. Je třeba ale mít na paměti, že zatímco všechny ostatní suroviny mohou být silnějšími agenty kombinovány v jejich batozích, vodu může každý agent nést jen jeden díl a k ní žádnou jinou surovinu.

Druidí klany mohou vytvářet koalice. Každý kněz může kdykoliv navrhnout koalici tak, že provede akcí propose s parametry, které vyjadřují podíl na výhře pro jednotlivé koalice. Počet parametrů (termů) musí tedy odpovídat počtu klanů ve hře. Letos tento počet bude pevně dán a klany budou vždy čtyři. Také může kněz přijmout koalici provedením akce accept s parametrem jméno klanu, který koalici navrhuje - viz vjemy a akce. Pokud všechny klany, které mají v navržené koalici nenulový podíl souhlasí, je koalice platná a hra končí, pokud koalice v součtu dosáhne cílové částky. Potom se také patřičně rozdělí počet bodů za výhru. Koalice zaniká, pokud kterýkoliv z kněží navrhne jinou koalici, nebo jinou koalici příjme.

    tato čísla můžou být ještě pozměněna

Schopnosti agentů jsou následující:
Agent	Pohybové body	Kapacita	Rozhled
aPriest	1	0	0
aBroad	1	4*sa(m)	1
aSharpSight	2	1	3*sa(s)
aLong	3*sa(f)	2	1

sa(s) je rovno jedné na začátku, pokud Bystrozraký během hry vezme brýle, pak je sa(s) rovno dvoum. Stejně tak sa(f) a sa(m) se mohou zvýšit z jedné na dvou, pokud dlouhý sebere boty, nebo široký rukavice.

V každém cyklu agent obdrží od prostředí vjemy a může na prostředí působit tolika akcemi, kolik odpovídá jeho počtu tahů z výše uvedené tabulky. Vjemy z prostředí jsou umístěny do agentovy báze znalostí. Následující tabulka udává pod sloupci název a argumenty predikátový symbol a typy termů, které se v predikátu reprezentujícím znalost vyskytují.
Název	Argumenty	Význam
team	char name	Název klanu.
coalitionProposal	char name, int s1, int s2, int s3, int s4	Klan name navrhuje koalici s podíly s1 .. s4.
coalition	char name, int s1, int s2, int s3, int s4	Přijata koalice navržená klanem name navrhuje koalici s podíly s1
carrying capacity	int x	Agent má možnost nést maximálně x surovin.
bag	seznam	pokud má agent kapacitu něco nést (není druid) v seznamu je položka wood/stone/water/gold nebo null, pokud je toto místo v batohu volné
bagfull		Batoh je plný
obstacle	int x, int y	Na pozici /x; y/ je překážka.
gold	int x, int y	Na pozici /x; y/ je zlato.
wood	int x, int y	Na pozici /x; y/ je dřevo.
spectacles	int x, int y	Na pozici /x; y/ jsou brýle.
gloves	int x, int y	Na pozici /x; y/ jsou rukavice.
enemy	int x, int y	Na pozici /x; y/ je nepřítel.
ally	int x, int y	Na pozici /x; y/ je přítel.
depot	int x, int y	Zlato se nosí na pozici /x; y/.
friend	string A	Mým přítelem je agent A.
grid size	int x, int y	Prostředí má rozměry x na y.
moves left	int x	Agentu zbývá x pohybů v tomto kole.
moves per round	int x	Tento typ agenta má x pohybů na kolo.
pos	int x, int y	Pozice agenta je y.
step	int x	Nacházíme se v x-tém kole.

Druidovy vjemy se liší a jsou následující
Název	Argumenty	Význam
depot	objekt int x	V depotu se nachází x kusů suroviny dané objektem (wood, gold, water, stone, pergamen)
money	us|them int x	Náš nebo soupeřův tým vydělal obnos x jednotek měny
spell	int st, int wt, int wd, int gd	K vytvoření předmětu je potřeba st/wt/wd/gd jednotek kamene/vody/dřeva/zlata

Odpovědí agenta na aktuální stav je provedení akce nebo akcí. Agent musí v každém kole vypotřebovat všechny svoje pohybové body! Pokud agent nechce provést žádnou akci (je pro něj výhodné zůstat na pozici), lze využít akce do(skip). Obdobně jako u vjemů i u akcí uvedeme tabulku ze které poznáte, jaké akce agenti mohou provádět.
Název	Argumenty	Cena(PB)	Význam
do(up)		- 1	Přesune agenta nahoru.
do(down)		- 1	Přesune agenta dolů.
do(left)		- 1	Přesune agenta doleva.
do(right)		- 1	Přesune agenta doprava.
do(skip)		- 1	Prázdná akce.
do(pick)		- max (1,2,3)	Z aktu alní pozice vezme surovinu rukavoce, boty, nebo brýle. Brýle může zvednout pouze Bystrozraký, boty pouze Dlouhý, rukavice pouze Široký
do(dig, x)	x je z množiny {n,s,w,e}	- max (1,2,3)	Agent sebere (vykope) kámen, pokud je od něj v zadaném směru
drop(X)	viz ->	- max (1,2,3)	Na aktualní pozici (musí být depot) polož surovinu/suroviny ze svého batohu. Pokud X je z {"gold","wood","water","stone","pergamen"}. Pokud X je "all" odloží do depotu vše z batohu.

Po provedení akcí pick, drop a dig přijde agent o všechny pohybové body, které má pro dané kolo k dispozici. Kněz může vykonávat poze následující čtyři akce
Název	Argumenty	Cena(PB)	Význam
do(read,n)	n je z intervalu <3,5>	-1	Přečte n pergamenů, uspěje, pokud jich tolik má v depotu. Výsledkem může být nová kombinace surovin k vytvoření předmětu v daném počtu.
do(create, st,wt,wd,gd)	st,wt,wd a gd jsou z intervalu <0,5>	-1	Pokusí se vytvořit předmět z uvedené kombinace surovin
do(propose, share1,share2 ...)	share jsou z <0,99>, jejich suma musí být rovna 100	-1	Navrhne koalici s podíly share1 ... , počet share musí odpovídat počtu klanů. Pokud je share 0 pro nějaký klan, není tento ke koalici přizváván
do(accept, clanName)	clanName z {"a","b"...}	-1	Kněz přijímá za koalici klanu koalici navrhovanou klanem clanName

