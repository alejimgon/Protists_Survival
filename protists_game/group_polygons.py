EUK_GROUP_SELECTION_IMAGES = {
    "Metamonada": "images/screen_images/metamonada/metamonada_selection.png",
    "TSAR": "",
    "Cryptista": "",
    "Archaeplastida": "",
    "Haptista": "",
    "Amorphea": "",
    "CRuMs": "",
    "Ancoracysta": "",
    "Picozoa": "",
    "Discoba": "",
    "Ancyromonadida": "",
    "Hemimastigophora": "",
}

PROTIST_INFO_IMAGES = {
    "Metamonada": {
        "Giardia intestinalis": "images/screen_images/metamonada/metamonada_selection_gintestinalis.png",
        "Giardia muris": "images/screen_images/metamonada/metamonada_selection_gmuris.png",
        "Spironucleus salmonicida": "images/screen_images/metamonada/metamonada_selection_ssalmonicida.png",
        "Trepomonas sp.": "images/screen_images/metamonada/metamonada_selection_trepomonas.png",
        "Hexamita inflata": "images/screen_images/metamonada/metamonada_selection_hinflata.png",
        "Trichomonas vaginalis": "images/screen_images/metamonada/metamonada_selection_tvaginalis.png",
        "Kipferlia bialata": "images/screen_images/metamonada/metamonada_selection_kbialata.png",
        "Monocercomonoides exilis": "images/screen_images/metamonada/metamonada_selection_mexilis.png"
    },
    # Add more as you create them
}

PROTIST_BACKGROUND_IMAGES = {
    "Giardia intestinalis": "images/background/small_intestine.png",
    "Giardia muris": "images/background/small_intestine.png",
    "Spironucleus salmonicida": "images/background/small_intestine.png",
    "Monocercomonoides exilis": "images/background/small_intestine.png",
    "Trichomonas vaginalis": "images/background/vaginal_epithelium.png",
}

EUK_GROUP_SELECTION_POLYGONS = {
    "Metamonada": [
        (783, 643), (795, 628), (880, 692), (867, 712)
    ],
    "TSAR": [
        (285, 65), (538, 65), (538, 308), (439, 371), (285, 252)
    ],
    "Cryptista": [
        (554, 23), (750, 23), (750, 139), (671, 301), (554, 279)
    ],
    "Archaeplastida": [
        (803, 130), (953, 130), (953, 430), (758, 430), (680, 300)
    ],
    "Haptista": [
        (115, 283), (234, 283), (405, 361), (400, 480), (115, 480)
    ],
    "Amorphea": [
        (392, 567), (550, 645), (511, 857), (243, 857), (243, 670)
    ],
    "CRuMs": [
        (558, 641), (668, 622), (763, 792), (763, 857), (558, 857)
    ],
    "Ancoracysta": [
        (190, 536), (300, 513), (305, 536), (196, 559)
    ],
    "Picozoa": [
        (252, 603), (315, 570), (326, 592), (261, 624)
    ],
    "Discoba": [
        (754, 673), (799, 728), (785, 744), (737, 687)
    ],
    "Ancyromonadida": [
        (840, 511), (983, 543), (978, 566), (836, 533)
    ],
    "Hemimastigophora": [
        (848, 449), (1003, 449), (1003, 476), (848, 476)
    ],
    "Malawimonadida": [
        (816, 592), (825, 572), (951, 632), (942, 653)
    ],
}

PROTIST_SELECTION_POLYGONS = {
    "Metamonada": {
        "Giardia intestinalis": [
            (123, 321), (319, 321), (319, 500), (123, 500)
        ],
        "Giardia muris": [
            (319, 321), (515, 321), (515, 500), (319, 500)
        ],
        "Spironucleus salmonicida": [
            (515, 321), (711, 321), (711, 500), (515, 500)
        ],
        "Trepomonas sp.": [
            (221, 680), (417, 680), (417, 859), (221, 859)
        ],
        "Hexamita inflata": [
            (417, 680), (613, 680), (613, 859), (417, 859)
        ],
        "Trichomonas vaginalis": [
            (515, 500), (711, 500), (711, 680), (515, 680)
        ],
        "Kipferlia bialata": [
            (319, 500), (515, 500), (515, 680), (319, 680)
        ],
        "Monocercomonoides exilis": [
            (123, 500), (319, 500), (319, 680), (123, 680)
        ],
    },
    # Add more as you create them
}

BOTTONS_POLYGONS = {
    "Metamonada_screen": {
        "back": [
            (1186, 830), (1330, 830), (1330, 870), (1186, 870)
        ],
    }
}

GROUP_ALLOWED_ENERGY = {
    "Metamonada": ['glucose', 'fructose', 'arginine', 'bacteria']
    # etc.
}

GROUP_ALLOWED_DANGER = {
    "Metamonada": ['ROS']
    # etc.
}