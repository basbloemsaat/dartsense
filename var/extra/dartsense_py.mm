<map version="freeplane 1.6.0">
<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net -->
<node TEXT="Dartsense site" FOLDED="false" ID="ID_1379987561" CREATED="1506241086498" MODIFIED="1506241171196" STYLE="oval">
<font SIZE="18"/>
<hook NAME="MapStyle">
    <properties edgeColorConfiguration="#808080ff,#ff0000ff,#0000ffff,#00ff00ff,#ff00ffff,#00ffffff,#7c0000ff,#00007cff,#007c00ff,#7c007cff,#007c7cff,#7c7c00ff" fit_to_viewport="false"/>

<map_styles>
<stylenode LOCALIZED_TEXT="styles.root_node" STYLE="oval" UNIFORM_SHAPE="true" VGAP_QUANTITY="24.0 pt">
<font SIZE="24"/>
<stylenode LOCALIZED_TEXT="styles.predefined" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="default" ICON_SIZE="12.0 pt" COLOR="#000000" STYLE="fork">
<font NAME="SansSerif" SIZE="10" BOLD="false" ITALIC="false"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.details"/>
<stylenode LOCALIZED_TEXT="defaultstyle.attributes">
<font SIZE="9"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.note" COLOR="#000000" BACKGROUND_COLOR="#ffffff" TEXT_ALIGN="LEFT"/>
<stylenode LOCALIZED_TEXT="defaultstyle.floating">
<edge STYLE="hide_edge"/>
<cloud COLOR="#f0f0f0" SHAPE="ROUND_RECT"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.user-defined" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="styles.topic" COLOR="#18898b" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subtopic" COLOR="#cc3300" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subsubtopic" COLOR="#669900">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.important">
<icon BUILTIN="yes"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.AutomaticLayout" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="AutomaticLayout.level.root" COLOR="#000000" STYLE="oval" SHAPE_HORIZONTAL_MARGIN="10.0 pt" SHAPE_VERTICAL_MARGIN="10.0 pt">
<font SIZE="18"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,1" COLOR="#0033ff">
<font SIZE="16"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,2" COLOR="#00b439">
<font SIZE="14"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,3" COLOR="#990000">
<font SIZE="12"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,4" COLOR="#111111">
<font SIZE="10"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,5"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,6"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,7"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,8"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,9"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,10"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,11"/>
</stylenode>
</stylenode>
</map_styles>
</hook>
<hook NAME="AutomaticEdgeColor" COUNTER="3" RULE="ON_BRANCH_CREATION"/>
<node TEXT="parse de excelfiles naar een sqlite database" POSITION="right" ID="ID_1072196996" CREATED="1506241172612" MODIFIED="1506241195500">
<edge COLOR="#ff0000"/>
<node TEXT="schrijf naar sqlite" ID="ID_1648195034" CREATED="1506241256569" MODIFIED="1506241262404"/>
<node TEXT="database contents" ID="ID_1830994600" CREATED="1506241278928" MODIFIED="1506241287884">
<node TEXT="vanuit excel" ID="ID_382592634" CREATED="1506241288331" MODIFIED="1506241292535"/>
<node TEXT="aliassen voor spelers (zijn verschillend per jaar)" ID="ID_152519723" CREATED="1506241292888" MODIFIED="1506241314436"/>
<node TEXT="baannummer 1 tm 6, overig is onbekend (99, ? en NULL gebruikt voor onbekend)" ID="ID_430226257" CREATED="1506241519874" MODIFIED="1506241613087"/>
<node TEXT="rondenummer alles onder 1 en boven de 50 is onbekend/bye (99, ? en 0 gebruikt voor bye)" ID="ID_554667309" CREATED="1506241537187" MODIFIED="1506241595203"/>
<node TEXT="rating, berekend bij inlezen" ID="ID_480229000" CREATED="1506241637853" MODIFIED="1506241645240"/>
</node>
<node TEXT="database structuur" ID="ID_608580210" CREATED="1506241337734" MODIFIED="1506241343071">
<node TEXT="speler" ID="ID_1043550439" CREATED="1506241343855" MODIFIED="1506241345840"/>
<node TEXT="wedstrijd" ID="ID_536329390" CREATED="1506241346525" MODIFIED="1506241353063"/>
</node>
</node>
<node TEXT="flask site om de stats te tonen" POSITION="right" ID="ID_1423176291" CREATED="1506241199559" MODIFIED="1506241213594">
<edge COLOR="#00ff00"/>
<node TEXT="dartsense.nl/SVAusterlitz" ID="ID_1233705187" CREATED="1506241436556" MODIFIED="1506241468331"/>
</node>
</node>
</map>
