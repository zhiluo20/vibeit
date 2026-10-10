"""Plain-language narration layered over the unchanged experimental workflows."""
from ._common import bilingual
from pathlib import Path
import base64

GUIDANCE = {
    'goal': bilingual(
        '## Start here: a story, then pictures\n\nYou can understand the story and explore the pictures without knowing biology or Python. If you want to run or change the code, ask a teacher or someone who knows basic Python to join you.\n\n**Three words to know.** A **protein** is a long chain of small building blocks folded into a 3D shape. Each building block is an **amino acid**; inside a protein, scientists also call it a **residue**. An **atom** is a much smaller part of a building block. Think of beads made from even tinier pieces. Real proteins can bend and move, so the bead-and-block picture is only a helpful comparison.\n\n**Two ways to learn.** To follow the story, read the short explanations and look at the pictures; code and extra technical notes can wait. To do the experiment on your device, download the whole `.ipynb`, use **+ → Import from Files** in VibeIt, and run every code cell from top to bottom.\n\nThe charts and interactive molecular models below are actual saved code outputs. The hand-drawn sketches only explain an idea; they are not experimental structures. The data and sketches are packed inside the notebook, with no extra data file to find. Save it in your working folder. You do not need an AI account.',
        '## 从这里开始：先听故事，再看图片\n\n没学过生物、没写过 Python，也可以先读懂故事、看看图片。想运行或修改代码时，可以请会一点 Python 的老师或同学一起做。\n\n**先认识三个词。** **蛋白质**可以想成一长串小珠子折成的三维物体。每颗珠子对应一个**氨基酸**，在蛋白质里也叫**残基**。**原子**是组成珠子的更小部件。真实的蛋白质会弯、会动，珠子和积木只是帮助理解的比方。\n\n**两种学法。** 想先听懂，就读短讲解、看图片；代码和“多学一点”可以以后再看。想在设备上做一遍，就下载完整 `.ipynb`，在 VibeIt 中点 **+ → Import from Files**，然后从上到下运行所有代码单元。\n\n下面的统计图和可旋转分子模型，来自代码的实际运行；简笔画只用来说明原理，不是实验结构。数据和简笔画已经装在 notebook 里面，不用另找文件。把 notebook 保存在当前工作文件夹即可；这节课不需要 AI 账号。'),
    'setup': bilingual('## Let the tools get ready','## 让工具先准备好'),
    'load': bilingual(
        '### Open the data packed inside this notebook\n\nThink of the notebook as a school bag: the instructions and the data are packed together. The next code finds that bag and checks its data label. That check is called SHA-256; you do not need to memorize the name. Renaming the notebook is fine. Keep it saved in the current folder. If it cannot be found, check the folder first. Copying only the code leaves the data behind.',
        '### 打开 notebook 里面的数据包\n\n把 notebook 想成书包：讲解和数据都装在里面。下面的代码找到书包，再核对数据的“标签”，确认没有拿错。这个核对方法叫 SHA-256，现在不用记住名字。文件改名也能识别，但要保存在当前工作文件夹。找不到时，先检查文件位置；只复制代码，会把数据包落下。'),
    'methods': bilingual(
        '### Our reusable tools\n\nThe next four pieces of code are like tools in a pencil case: read the 3D file, measure distances, keep the labels, and prepare a model to show. You can skip reading their internals while following the story. When running the notebook, run them in order so the tools are ready for later steps.',
        '### 准备几个会反复用到的小工具\n\n下面四段代码像文具盒里的工具：读三维文件、量距离、保留编号、准备显示模型。听故事时可以先不读代码里面的细节；实际运行 notebook 时，要按顺序运行，让后面用到的工具准备好。'),
    'data_heading': bilingual('### What is in our model?','### 今天的模型里有什么？'),
    'steps': bilingual('## Follow the story and try it','## 一起看图、动手试试'),
    'online': bilingual(
        '## Optional: check the source online\n\nYou can skip this. The switch below starts as `False`, which means off. The lesson already has its data. Turning the switch on only checks the source website; it does not replace our data. If the internet is unavailable, keep using the packed data. A new dataset would need its own date, label and checks.',
        '## 可选：联网看看数据来源\n\n这一段可以跳过。下面的开关默认是 `False`，意思是“关闭”。本课的数据已经备好；打开开关只会查看来源网站，不会换掉当前数据。联网失败时，继续用原来的数据即可。以后换一份新数据，需要重新记录日期、标签并核对结果。'),
    'next': bilingual(
        '**What next?** Explain the pictures to someone else in your own words. Then try one small change and compare the old and new results. If you use another real structure, first check what it contains and whether the components share a meaningful position in space.',
        '**接下来做什么？** 先用自己的话，把图片讲给另一个人听。再试着改一个小参数，比较前后结果。换成其他真实结构时，先确认里面是谁，以及各部分在空间中的位置是否真的能放在一起比较。'),
}


def note_ref(number):
    return f'<a class="note-ref-link" href="#reading-note-{number}"><sup class="note-ref">{number}</sup></a>'


def clean_explanation(text, locale):
    """Keep the reading flow direct; method qualifications live in the endnotes."""
    changes = {
        'en': [
            ('It does not show the whole antibody or a whole cell.', ''),
            ('The hand-drawn sketches only explain an idea; they are not experimental structures.', ''),
            ('More neighbors do not show stronger binding.', 'The neighbor count follows the chosen distance boundary.'),
            ('Existing experiments tell us about that effect; today we are looking at', 'Today we are looking at'),
            ('Real proteins can bend and move, so the bead-and-block picture is only a helpful comparison.', 'Real proteins can bend and move.'),
            ('It was taken out of the same model for easier viewing; it is not a new prediction of how a free drug floats in water.', 'It was taken out of the same model for easier viewing.'),
            ('They are not real cloth.', ''),
            ('Stick connections help us draw the molecule; they do not tell us how strongly it binds.', 'Stick connections help us follow the molecule’s shape.'),
            ('A/B are labels, not a ranking.', 'A/B are labels that help us choose a copy.'),
            ('Some parts were too hard to locate clearly in the experiment; we do not invent positions for them.', 'The experiment recorded usable positions for some parts of the protein.'),
            ('The nearest block is not automatically the most important one.', ''),
            ('A close pair is a clue, not proof of a chemical bond. Two people standing near each other are not necessarily holding hands. Scientists need other information before naming the type of interaction.', ''),
            ('It is not a curve of giving more medicine.', ''),
            ('We still need separate experiments to find how tightly it binds and how it affects the protein’s work.', 'A possible next step is to measure binding and protein activity in an experiment.'),
            ('That describes where they are, not how powerful the drug is.', 'I can use the picture and table to show where they are.'),
            ('It is only a piece of the full antibody.', 'Fab is the antibody’s binding piece.'),
            ('The hand-and-block picture is a comparison. Real proteins bend and move; this model shows one experimentally observed arrangement.', 'Turn the model to see the meeting place from different directions.'),
            ('“Light” and “heavy” are chain names, not a contest about which one matters more.', '“Light” and “heavy” are the names of the two chains.'),
            ('It is not our antibody drug.', ''),
            ('Its axes are just directions in the saved model, not “up” or “down” inside a person.', 'Its axes record positions in the saved model.'),
            ('We leave sugars and water out of this particular protein-interface picture. That is a choice about what to look at; it does not mean they never matter.', 'This view focuses on the protein chains.'),
            ('This does not tell us which chain binds more strongly.', ''),
            ('A close pair is a location clue. Calling it a hydrogen bond or an especially important binding point needs more information and experiments.', ''),
            ('We do not fill the gap with an invented dot.', ''),
            ('Do not compare the small drug and the much bigger antibody by contact totals alone. A large hand has more opportunities to be near something than a tiny finger. A bigger count does not by itself tell us how tightly a drug binds.', 'The small drug and the larger antibody have different sizes and arrangements. Compare their pictures as well as their counts.'),
            ('Do not draw imaginary neighbors just to make the picture look busy.', ''),
            ('Both lessons measure who is near whom, but counting neighbors alone does not prove a medicine’s effect.', 'Both lessons measure who is near whom.'),
        ],
        'zh-hans': [
            ('图里不是完整抗体，也不是整个细胞。', ''),
            ('简笔画只用来说明原理，不是实验结构。', ''),
            ('邻居多了，不能证明结合更牢。', '近邻数量随选定的距离边界变化。'),
            ('这个作用是已有实验告诉我们的；今天我们先看看：', '转动模型，我们可以看看：'),
            ('真实的蛋白质会弯、会动，珠子和积木只是帮助理解的比方。', '真实的蛋白质会弯、会动。'),
            ('它像盒子标签，帮助我们避免拿错。', '它像盒子标签，帮助我们认清内容。'),
            ('A/B 是标签，不是优劣排名。', 'A/B 是标签，帮助我们选定一份蛋白。'),
            ('有些部件在实验中没有看清位置，我们不会替它编一个位置。', '这份文件记录了实验中看清位置的部件。'),
            ('方便看清；不是另算出来的“游离药物在水里怎样飘”。', '方便看清。'),
            ('丝带只是方便看清蛋白形状的画法，不是真的布。', '丝带帮助我们看清蛋白的走向。'),
            ('细棒连接帮助我们画分子，不能告诉我们它结合得有多牢。', '细棒连接帮助我们看清分子的形状。'),
            ('离得最近，不等于作用一定最大。', ''),
            ('靠得近是一条线索，不等于一定形成了某种化学连接。就像两个人站得近，不代表他们正在握手。要给连接起专业名字，还得知道别的信息。', ''),
            ('这条曲线不是“吃更多药会怎样”的曲线。', ''),
            ('想知道它结合得多牢、怎样影响蛋白工作，还需要另外的实验。', '下一步可以通过实验测量结合情况和蛋白的工作状态。'),
            ('这描述它们的位置，不能说明药物有多厉害。', '我可以用图片和表格，指出它们的位置。'),
            ('叫 **Fab**，不是完整抗体。', '叫 **Fab**。'),
            ('“手”和“积木”只是比方。真实蛋白质会动，这个模型展示实验中观察到的一种摆放样子。', '转动模型，从不同方向观察相遇的位置。'),
            ('“轻”和“重”是名称，不是在比赛谁更重要。', '“轻”和“重”是这两条链的名称。'),
            ('它不是今天的抗体药物。', ''),
            ('坐标轴只是模型里记位置的方向，不代表人体里的“上面”和“下面”。', '坐标轴帮助我们记录模型中的位置。'),
            ('这张蛋白接触图暂时省略糖和水，是为了专心看两边蛋白，不能因此说糖和水永远不重要。', '这张图专心展示两边的蛋白链。'),
            ('两条链都参与了接触，但不能据此说哪条链结合得更牢。', '两条链都参与了接触。'),
            ('近距离告诉我们“这里可能值得研究”。要叫它氢键，或说它是特别重要的结合点，还需要别的信息和实验。', ''),
            ('我们不凭空补点。', ''),
            ('也别只看接触总数，就比较小药物和大抗体谁更牢。就像一只大手比一根小手指，有更多地方可能挨近东西，但仅凭数量不能知道“握得多紧”。', '小药物和大抗体的大小、摆放方式不同。可以把图片和计数放在一起比较。'),
            ('不用为了让图热闹，就画出不存在的邻居。', ''),
            ('两课都在量谁靠近谁，但只数邻居，不能证明药物的作用。', '两课都在量谁靠近谁。'),
        ],
    }
    for before,after in changes[locale]:
        text=text.replace(before,after)
    return text.strip()


LESSONS = {
    '07-imatinib-pocket': [
        ('A small piece and a much bigger machine','一块小积木，怎样影响一台大机器？',
         'Imagine a machine with a small groove where a working part fits. A protein called **ABL** has a place used by a small molecule called ATP. The drug **imatinib** fits in a related pocket and helps ABL stay in a shape that is not working. Existing experiments tell us about that effect; today we are looking at **where the drug sits and what is near it**.\n\nThink of hemoglobin’s heme as a normal working part of a machine. Here we look at a drug that gets in the way of the machine’s work. Real proteins move, so they are more flexible than toy blocks.\n\n**Try saying it:** “Today we will find the drug and its nearby protein parts.”',
         '想象一台机器上有个小凹槽，平时有个工作零件放在那里。名叫 **ABL** 的蛋白质，也有用到 ATP 这个小分子的位置。**伊马替尼**这个药物会占住相关的口袋，让 ABL 更容易保持不工作的形状。这个作用是已有实验告诉我们的；今天我们先看看：**药物坐在哪里，旁边有谁？**\n\n前面见过的血红素，像机器本来就需要的工作部件。这里的药物，则会影响机器工作。真实蛋白质会动，比硬积木灵活得多。\n\n**试着说一句：**“今天要找到药物和它旁边的蛋白小部件。”'),
        ('Check the label before opening the box','先看盒子标签，认清里面是谁',
         'This model is a **lab-made picture of part of a mouse ABL protein together with imatinib**. Scientists call the file 1IEP. You do not need to remember that code. It keeps us from using the wrong picture.\n\nThe file contains two similar protein copies, labelled A and B. We look at **A and its own drug**. A/B are labels, not a ranking. The drug’s file label is STI. Some parts were too hard to locate clearly in the experiment; we do not invent positions for them.\n\n**Read the table:** `chain` is the copy label. For A, the recorded sequence has 293 building blocks, while positions for 274 Cα reference points were observed. Those two counts answer different questions.',
         '今天的模型，是科学家通过实验得到的：**小鼠 ABL 蛋白的一部分，和伊马替尼放在一起的样子**。文件编号叫 1IEP，不用背；它像盒子标签，帮助我们避免拿错。\n\n文件里有两份相似的蛋白，标成 A、B。我们只看 **A 和它自己的药物**。A/B 是标签，不是优劣排名。药物在文件里叫 STI。有些部件在实验中没有看清位置，我们不会替它编一个位置。\n\n**表格这样读：**`chain` 是标签。A 的说明记录了 293 个小部件，但实验图里能找到 274 个 Cα 参考点的位置；两个数字数的东西不同。Cα 是每颗珠子中用来标位置的一个特定原子。'),
        ('Turn the model and find the orange drug','转一转，找出橙色的药物',
         '**First picture:** the drug alone, shown in its experimentally observed position and shape. It was taken out of the same model for easier viewing; it is not a new prediction of how a free drug floats in water.\n\n**Second picture:** green ribbons show the larger ABL protein, and orange sticks show the drug. The ribbons are a drawing style that helps us follow the protein’s shape. They are not real cloth.\n\n**Try it:** turn and zoom the model. Find the orange piece, then see how much larger the green protein is. Stick connections help us draw the molecule; they do not tell us how strongly it binds.',
         '**第一幅图：**单独看药物。它的形状和位置，是从同一个实验模型里取出来的，方便看清；不是另算出来的“游离药物在水里怎样飘”。\n\n**第二幅图：**绿色丝带是较大的 ABL 蛋白，橙色细棒是药物。丝带只是方便看清蛋白形状的画法，不是真的布。\n\n**动手试试：**转动、放大模型，先找到橙色，再看绿色部分比它大多少。细棒连接帮助我们画分子，不能告诉我们它结合得有多牢。'),
        ('Find the drug’s close neighbors','给药物找“近邻”',
         'Imagine circling the neighbors who live close to your house. We do something similar for the drug: **which protein building blocks have any small part close enough to it?** We measure the shortest straight-line distance between their atoms and the drug’s atoms.\n\nOur rule is **at most 4 Å**. Å is a very tiny unit of length. You do not need to memorize the conversion now; 4 Å is just the boundary we chose. We find **21 protein building blocks** inside it.\n\n**Read the bars:** one bar is one block. A shorter bar means a smaller nearest distance. The dashed line marks 4 Å. `label` is the block’s name and number; `min_distance_A` is its nearest distance. The nearest block is not automatically the most important one.',
         '想象你在地图上，圈出住在家附近的邻居。我们也给药物找近邻：**哪些蛋白小部件，有某个小点离药物足够近？**量的是两边原子之间最近的直线距离。\n\n这次约定：**距离不超过 4 Å 就算近邻**。Å 是很小很小的长度单位，现在不用背换算；先把 4 Å 当成我们画的边界。按这个规则，找到 **21 个蛋白小部件**。\n\n**柱形图这样看：**一条柱子代表一个部件；柱子越短，最近距离越小。虚线是 4 Å 的边界。表中 `label` 是部件名称和编号，`min_distance_A` 是最近距离。离得最近，不等于作用一定最大。'),
        ('Use colors as a distance ruler','把颜色表当成一把距离尺',
         'This picture is a table made of colored squares. A **row** is one drug atom; a **column** is one nearby protein block. Each square answers: “How close is this drug atom to the nearest atom in that block?”\n\n**Yellow means closer; blue/purple means farther.** Use the color bar at the right as a ruler. Values above 8 Å share the far-end color, so they cannot be distinguished by color alone.\n\nA close pair is a clue, not proof of a chemical bond. Two people standing near each other are not necessarily holding hands. Scientists need other information before naming the type of interaction.',
         '这张图是一张由彩色小格子组成的表。**一行**是药物的一个原子，**一列**是蛋白的一个近邻部件。每格回答：“这个药物原子，离这个部件中最近的原子有多远？”\n\n**黄色偏近，蓝紫色偏远。**右边的色条就是尺子。超过 8 Å 的值会显示同一个最远颜色，仅凭颜色分不出谁更远。\n\n靠得近是一条线索，不等于一定形成了某种化学连接。就像两个人站得近，不代表他们正在握手。要给连接起专业名字，还得知道别的信息。'),
        ('A long bead chain can fold around a small piece','长珠子串折起来，可以围住一块小积木',
         '**In the dot picture:** green dots mark reference positions in the protein, orange dots mark drug atoms, and purple dots mark the selected nearby blocks. The protein chain folds in space, so blocks far apart along the chain can end up near the same drug.\n\n**In the close-up:** purple sticks show the nearby protein atoms and orange sticks show the drug. A label such as `A:THR315` is an address: copy A, block type THR, number 315. You do not have to memorize the letters.\n\nTry rotating the model. The view changes, but the distances do not. Turning a map does not move the houses on it.',
         '**散点图里：**绿点标出蛋白中的参考位置，橙点是药物原子，紫点标出选中的近邻部件。长珠子串折起来以后，串上相隔很远的珠子，也可能一起围住药物。\n\n**局部放大图里：**紫色细棒是附近的蛋白原子，橙色细棒是药物。`A:THR315` 这样的标签像地址：A 这份蛋白里，编号 315、类型叫 THR 的部件。不用背这些字母。\n\n转一转模型：看的方向变了，真实距离没变。就像转动一张地图，不会把房子搬走。'),
        ('A bigger circle includes more neighbors','圈画得大一点，邻居会多一点',
         'Change the neighbor rule from 4 Å to 5 Å. A wider boundary may include more blocks, even though **the drug and protein did not move**. The curve shows this change in our counting rule. It is not a curve of giving more medicine.\n\n**Read the curve:** along the bottom is the distance boundary; up the side is the number of neighbors. Making the boundary larger cannot remove a neighbor.\n\nWhat did we learn? We located the drug and described its neighborhood. We still need separate experiments to find how tightly it binds and how it affects the protein’s work.',
         '把近邻规则从 4 Å 改成 5 Å，圈画得宽一些，可能会多算几个部件。**药物和蛋白并没有移动**，变的是我们的计数规则。这条曲线不是“吃更多药会怎样”的曲线。\n\n**曲线这样看：**横着是距离边界，竖着是邻居数量。圈变大，原来的邻居不会被排除。\n\n我们学到了什么？找到了药物，描述了它周围的部件。想知道它结合得多牢、怎样影响蛋白工作，还需要另外的实验。'),
        ('Check the ruler and save your work','检查尺子，再把结果装进文件夹',
         'We do two simple checks. First, measure one nearest pair again another way. Second, move the whole model together: distances must stay the same, just as moving an entire toy house does not change the gaps between its blocks.\n\nThe code saves tables, a model file and a short summary in `results/07-imatinib-pocket/`. CSV files are tables you can open later; PDB holds the selected 3D positions. An empty result is allowed when the chosen boundary is too small.\n\n**Tell someone:** “I found 21 neighboring protein blocks using the 4 Å rule. That describes where they are, not how powerful the drug is.”',
         '我们做两个容易理解的检查。第一，换一种办法，再量一次最近的那对小点。第二，把整个模型一起搬动：里面的距离应该不变，就像把积木房子整栋搬走，积木间的缝不会因此改变。\n\n代码把表格、模型文件和摘要保存在 `results/07-imatinib-pocket/`。CSV 是以后还能打开的表格；PDB 保存选中的三维位置。边界太小时，找不到近邻也是正常结果。\n\n**讲给别人听：**“用 4 Å 的规则，我找到了 21 个蛋白近邻部件。这描述它们的位置，不能说明药物有多厉害。”'),
    ],
    '08-trastuzumab-interface': [
        ('A shaped hand meets a protein surface','一只特别形状的“手”，怎样贴住蛋白表面？',
         'Last time a small drug fitted into a pocket. This time the drug is an **antibody**, which is itself a protein. Think of its binding part as a shaped hand that fits a particular place on another protein’s surface. The target protein here is called **HER2**.\n\nWe study the antibody’s gripping part, called **Fab**. It is only a piece of the full antibody. Our question is simple: **where do the two proteins meet, and which little building blocks are close?**\n\nThe hand-and-block picture is a comparison. Real proteins bend and move; this model shows one experimentally observed arrangement.',
         '上一课，小药物放进了蛋白的口袋。这一课的药物叫**抗体**，它本身也是蛋白质。可以把它负责结合的部分，想成一只有特别形状的“手”，能贴到另一个蛋白表面的合适位置。今天被它结合的蛋白，名字叫 **HER2**。\n\n我们只看抗体负责结合的一小部分，叫 **Fab**，不是完整抗体。问题很简单：**两者在哪里相遇，哪些小部件靠得近？**\n\n“手”和“积木”只是比方。真实蛋白质会动，这个模型展示实验中观察到的一种摆放样子。'),
        ('Give the three chains simple name tags','先给三个部分贴上名字标签',
         'The model’s file code is 1N8Z. Inside it, **A is the Fab light chain, B is the Fab heavy chain, and C is HER2**. A chain is a string of protein building blocks. “Light” and “heavy” are chain names, not a contest about which one matters more.\n\nHere the drug is made from protein chains, rather than one small molecule. The file also lists a sugar labelled NAG. It is not our antibody drug.\n\nA label can contain an extra letter, like a house address with an A added after the number. Keep that letter so two different blocks are not mistaken for one.',
         '模型的文件编号是 1N8Z。里面有三个标签：**A 是 Fab 轻链，B 是 Fab 重链，C 是 HER2**。“链”就是一串蛋白小部件。“轻”和“重”是名称，不是在比赛谁更重要。\n\n这里的药物由蛋白链组成，不是一个小分子。文件还列出一个叫 NAG 的糖，它不是今天的抗体药物。\n\n有些部件的编号后面带字母，像门牌号多了一个 A。这个字母要保留，才不会把两个不同部件当成同一个。'),
        ('Follow the green, orange and blue shapes','跟着绿色、橙色、蓝色认模型',
         '**Green is HER2. Orange is Fab light chain A. Blue is Fab heavy chain B.** Turn the model and find where orange and blue approach green. Do they sit all over it, or meet at a limited patch?\n\nThe dot picture below uses the same chain colors and helps show the overall arrangement. Its axes are just directions in the saved model, not “up” or “down” inside a person.\n\nWe leave sugars and water out of this particular protein-interface picture. That is a choice about what to look at; it does not mean they never matter.',
         '**绿色是 HER2，橙色是 Fab 轻链 A，蓝色是 Fab 重链 B。**转动模型，找找橙色和蓝色在哪里靠近绿色。它们是贴满整个蛋白，还是集中在一小块地方？\n\n下面的散点图沿用同样的颜色，方便看整体摆放。坐标轴只是模型里记位置的方向，不代表人体里的“上面”和“下面”。\n\n这张蛋白接触图暂时省略糖和水，是为了专心看两边蛋白，不能因此说糖和水永远不重要。'),
        ('Count the blocks and the pairs separately','小部件的数量，和“配对”的数量，要分开数',
         'Use the same **at most 4 Å** neighbor rule. Each pair is one Fab block and one HER2 block whose nearest atoms are close enough. We find **14 Fab blocks, 17 HER2 blocks and 32 close pairs**.\n\nWhy are the numbers different? Imagine three children each greeting two teachers. There are three children and two teachers, but six child–teacher pairs. One person can appear in more than one pair. Protein blocks can do the same.\n\n**Read the bars:** the orange bar counts 8 light-chain blocks; the blue bar counts 6 heavy-chain blocks. Both chains have neighbors across the meeting place. This does not tell us which chain binds more strongly.',
         '还是用**不超过 4 Å 就算近邻**的规则。一对，就是一个 Fab 部件和一个 HER2 部件，它们最近的原子靠得足够近。结果是：**14 个 Fab 部件、17 个 HER2 部件，组成 32 对近邻**。\n\n为什么数字不一样？想象三个小朋友，每人都和两位老师打招呼。小朋友有三个，老师有两位，但“小朋友—老师”的配对可以有六对。一个人可以出现在多对里，蛋白小部件也是一样。\n\n**柱形图这样读：**橙柱数到 8 个轻链部件，蓝柱数到 6 个重链部件。两条链都参与了接触，但不能据此说哪条链结合得更牢。'),
        ('Look for close pairs in the color table','在颜色表里找靠得近的配对',
         '**Rows are Fab blocks; columns are HER2 blocks.** A square shows the nearest atom distance for that pair. Yellow is closer; blue/purple is farther. Read the right-hand color ruler instead of guessing from the names.\n\nOnly blocks with at least one close partner are included in this picture. A block can be close to one partner and far from another, so the whole row need not be yellow. Distances above 8 Å share the far-end color.\n\nA close pair is a location clue. Calling it a hydrogen bond or an especially important binding point needs more information and experiments.',
         '**每一行是一个 Fab 部件，每一列是一个 HER2 部件。**每格显示这对部件的最近原子距离。黄色偏近，蓝紫色偏远；跟着右边的颜色尺读，不用猜名称是什么意思。\n\n图里只放入至少有一个近邻的部件。一个部件可以靠近这个伙伴，却离另一个较远，所以整行不一定都是黄色。超过 8 Å 的值会显示同一个最远颜色。\n\n近距离告诉我们“这里可能值得研究”。要叫它氢键，或说它是特别重要的结合点，还需要别的信息和实验。'),
        ('Find the meeting place along the bead chain','沿着珠子串，找相遇的小区域',
         'Imagine placing the HER2 building blocks in order like beads on a numbered string. This plot lets us follow that order. **Along the bottom is the HER2 block number; up the side is the distance to the nearest Fab atom.**\n\nGreen points show observed HER2 blocks. Purple points are within our 4 Å rule. Look for where the purple points gather: the close neighbors are concentrated in a limited part of the chain, not spread everywhere.\n\nA missing point means there was no usable position for that block. We do not fill the gap with an invented dot.',
         '想象把 HER2 的小部件，按顺序放成带编号的珠子串。这张图帮助我们沿着顺序找位置。**横轴是 HER2 部件的编号，纵轴是它到 Fab 最近原子的距离。**\n\n绿点是能在模型中找到位置的 HER2 部件；紫点符合 4 Å 的近邻规则。看看紫点在哪里聚集：近邻集中在串上的一小块区域，没有铺满整串。\n\n缺少的点，表示那个部件没有可用位置；我们不凭空补点。'),
        ('More neighbors does not mean a tighter grip','近邻更多，不一定“握得更牢”',
         'Make the boundary larger and you may count more neighbors. The model stays still; our counting rule changes. In the curve, separate lines count Fab blocks, HER2 blocks and pairs. They are different kinds of counts.\n\nDo not compare the small drug and the much bigger antibody by contact totals alone. A large hand has more opportunities to be near something than a tiny finger. A bigger count does not by itself tell us how tightly a drug binds.\n\nOur result describes a meeting place. To test how tightly the parts bind or how they change a cell’s behavior, scientists do separate experiments.',
         '把边界放大，可能数到更多近邻。模型没有动，变的是计数规则。曲线里的几条线，分别数 Fab 部件、HER2 部件和配对，它们数的不是同一种东西。\n\n也别只看接触总数，就比较小药物和大抗体谁更牢。就像一只大手比一根小手指，有更多地方可能挨近东西，但仅凭数量不能知道“握得多紧”。\n\n今天的结果描述两者相遇的地方。要知道它们结合得多牢，或怎样改变细胞的行为，科学家还要另做实验。'),
        ('Check the answer, save it, and tell the story','核对答案、保存结果，再讲一遍故事',
         'Measure one closest pair a second way, and move the whole model together to check that distances stay unchanged. Save the tables and model in `results/08-trastuzumab-interface/`.\n\nIf a boundary is too small to include any pair, an empty table is an honest answer. Do not draw imaginary neighbors just to make the picture look busy.\n\n**Tell someone:** “The small drug sits in a pocket. The antibody piece meets a protein surface. Both lessons measure who is near whom, but counting neighbors alone does not prove a medicine’s effect.”',
         '换一种办法核对最近的一对，再把整个模型一起搬动，检查距离有没有保持不变。把表格和模型存进 `results/08-trastuzumab-interface/`。\n\n如果边界太小，找不到配对，空表格就是诚实的答案。不用为了让图热闹，就画出不存在的邻居。\n\n**讲给别人听：**“小药物坐在口袋里；抗体的一部分贴在蛋白表面。两课都在量谁靠近谁，但只数邻居，不能证明药物的作用。”'),
    ],
}


def apply(courses, sections, exercises):
    for course in courses:
        identifier = course['id']
        course['plain_language'] = True
        course['illustration'] = 'drug-pocket-sketch.png' if course['number']==7 else 'antibody-surface-sketch.png'
        course['illustration_caption'] = bilingual(
            'Green is the protein and orange is the small drug. Top: identify the two parts. Bottom: see the drug in the pocket. Purple rings pick out nearby parts; the dashed line shows where a distance is measured.' if course['number']==7 else
            'Green is the target protein. Orange and blue show the two Fab chains approaching a local surface patch. Dashed lines show distances from a Fab part to a green target part.',
            '绿色是蛋白，橙色是小药物。上图认识两部分，下图看药物在口袋中的位置。紫圈选出附近的小部件，虚线标出量距离的位置。' if course['number']==7 else
            '绿色是靶蛋白，橙色和蓝色是 Fab 的两条链。它们在一小块表面相遇，虚线标出 Fab 部件与绿色靶蛋白部件之间的距离。')
        course['title'] = bilingual('How does a small drug fit into a protein pocket?' if course['number']==7 else
            'How does an antibody meet a protein surface?',
            '小药物怎样放进蛋白质口袋？' if course['number']==7 else '抗体怎样贴在蛋白质表面？')
        course['summary'] = bilingual(
            'Turn a real 3D model, find the drug and its neighbors, and learn what a distance measurement can tell us.' if course['number']==7 else
            'Follow three colors in a real 3D model and discover where an antibody piece meets its target protein.',
            '用伊马替尼与 ABL 的真实模型，像观察小积木放进凹槽一样，找到药物和它旁边的蛋白小部件。' if course['number']==7 else
            '用曲妥珠单抗与 HER2 的真实模型，跟着三种颜色，看看抗体的一部分怎样贴在蛋白表面。')
        prelude = bilingual(
            'Our model shows a piece of mouse ABL and a drug already observed together in an experiment. We study that picture rather than guessing a new position.' if course['number']==7 else
            'Our model shows the antibody’s Fab piece and part of HER2 already observed together in an experiment. It does not show the whole antibody or a whole cell.',
            '今天看的是小鼠 ABL 的一部分和药物在实验中一起出现的模型。我们研究这份真实记录，不随意猜一个新位置。' if course['number']==7 else
            '今天看的是抗体负责结合的 Fab 部分，和 HER2 的一部分在实验中一起出现的模型。图里不是完整抗体，也不是整个细胞。')
        course['reading_notes']=bilingual([
            'The teaching sketches use simplified shapes and bead counts. The molecular coordinates come from the cited PDB experimental record; the charts and interactive models retain their actual saved execution outputs.',
            '1IEP contains a mouse c-Abl kinase-domain construct and STI (imatinib), at 2.10 Å resolution. This lesson selects author chain A and its own ligand.' if course['number']==7 else '1N8Z contains human HER2 extracellular construct C and trastuzumab Fab light/heavy chains A/B, at 2.52 Å resolution. Trastuzumab is humanized; source-entity organism annotations describe the deposited construct.',
            'Distances are minimum Euclidean distances across positive-occupancy heavy atoms. The parser selects the first model and one alternate atom position; author chain, residue number and insertion code remain part of the identifier. The default neighbor boundary is 4 Å. The heatmap uses 2–8 Å and caps larger values at the far-end color.',
            'Binding strength, interaction chemistry and biological function are assessed with appropriate experimental evidence. Here, counts depend on the coordinate model and chosen distance boundary. Separate structure files require a reliable common spatial placement before cross-component distances are meaningful.'
        ],[
            '简笔画采用简化的形状和珠子数量。实验坐标来自所引 PDB 记录；统计图和可旋转模型保留了实际运行输出。',
            '1IEP 包含鼠源 c-Abl 激酶结构域构建体和 STI（伊马替尼），分辨率为 2.10 Å。本课选择作者链 A 及其自身配体。' if course['number']==7 else '1N8Z 包含人 HER2 胞外区构建体 C，以及曲妥珠单抗 Fab 轻链 A、重链 B，分辨率为 2.52 Å。曲妥珠单抗属于人源化抗体；来源实体的物种注释描述提交的构建体。',
            '距离取正占有率重原子对的最小欧氏距离。解析时选择第一个模型及一个替代原子位置；保留作者链、残基编号和插入码。默认近邻边界为 4 Å；热图色阶为 2–8 Å，更大的值使用最远端颜色。',
            '结合强度、相互作用类型和生物功能应结合相应实验证据评估。本课计数取决于坐标模型与距离边界。比较两个独立结构文件之前，需要建立可靠的共同空间定位。'
        ])
        for locale in ('en','zh-hans'):
            course['data_note'][locale] = clean_explanation(prelude[locale],locale) + note_ref(2)
        assert len(sections[identifier]) == len(LESSONS[identifier]) == 8
        for index, (old, (en_title,zh_title,en,zh)) in enumerate(zip(sections[identifier],LESSONS[identifier])):
            old['title'] = bilingual(en_title,zh_title)
            number=3 if index in (3,4,5) else (4 if index in (6,7) else 2)
            old['text'] = {locale: clean_explanation(text,locale)+note_ref(number)
                           for locale,text in [('en',en),('zh-hans',zh)]}
        if course['number']==8:
            root=Path(__file__).resolve().parents[1]/'illustrations'
            for locale in ('en','zh-hans'):
                raw=(root/('counting-pairs.'+locale+'.svg')).read_bytes()
                data=base64.b64encode(raw).decode()
                caption='Five people can make six greeting pairs.' if locale=='en' else '5位参与者，可以有6对打招呼关系。'
                picture=f'<figure class="principle-sketch"><img src="data:image/svg+xml;base64,{data}" alt="{caption}"><figcaption>{caption}{note_ref(1)}</figcaption></figure>'
                section=sections[identifier][3]
                section['text'][locale]+='\n\n'+picture
        # Keep the optional coding exercises, but make the independent questions conversational.
        new_questions = {
            '07-imatinib-pocket': bilingual(
                ['If we change the neighbor boundary from 4 to 5 Å, did we move the drug?',
                 'A person can reach out with a hand. Why would measuring from the body center miss a close fingertip?',
                 'We changed the counting rule, not the drug position. A protein side chain is like the reaching hand: an outer atom may be close even when its Cα reference atom is farther away. More neighbors do not show stronger binding.'],
                ['把近邻边界从 4 Å 改成 5 Å，药物真的移动了吗？',
                 '一个人伸出手时，只量身体中心的距离，为什么可能漏掉靠近的手指？',
                 '变的是计数规则，不是药物位置。蛋白的侧链像伸出的手：外面的原子可能很近，Cα 参考原子却更远。邻居多了，不能证明结合更牢。']),
            '08-trastuzumab-interface': bilingual(
                ['Three children each greet two teachers. How many people and how many child–teacher pairs are there?',
                 'What pairs remain if we use a very tiny 0.01 Å boundary?',
                 'There are five people and six pairs; people and pairs are different counts. At that boundary the picture and table show zero close pairs.'],
                ['三个小朋友，每人都和两位老师打招呼。总共几个人？可以组成几对“小朋友—老师”？',
                 '把边界缩到很小的 0.01 Å，表格里还会有哪些配对？',
                 '一共五个人，可以组成六对。人数和配对数是不同的计数。此时图与表格显示零近邻。']),
        }
        for locale in ('en','zh-hans'):
            previous=list(exercises[identifier][locale])
            previous[:3]=[clean_explanation(t,locale) for t in new_questions[identifier][locale]]
            exercises[identifier][locale]=previous
