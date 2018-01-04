from tetris.core.objects import *

prototypes = {
    'I': ProtoPiece(Color.RED,
        """
        .X..
        .X..
        .X..
        .X..
        """, 2),
    'J': ProtoPiece(Color.YELLOW,
        """
        ...
        XXX
        ..X
        """, 4),
    'L': ProtoPiece(Color.MAGENTA,
        """
        ...
        XXX
        X..
        """, 4),
    'O': ProtoPiece(Color.BLUE,
        """
        ....
        .XX.
        .XX.
        ....
        """, 1),
    'S': ProtoPiece(Color.CYAN,
        """
        ...
        .XX
        XX.
        """, 2),
    'T': ProtoPiece(Color.GREEN,
        """
        ...
        XXX
        .X.
        """, 4),
    'Z': ProtoPiece(Color.WHITE,
        """
        ...
        XX.
        .XX
        """, 2),
}

pieces = prototypes.values()

from tetris.core.game import Game