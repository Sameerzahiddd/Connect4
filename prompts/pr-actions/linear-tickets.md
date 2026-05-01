# LIN-5
**Title:** Add Expert difficulty level to minimax AI
**Body:** Add a fourth difficulty option (Expert) to the minimax AI that searches up to depth 7. Currently Hard only goes to depth 5, which experienced players can beat consistently. Expert should be a genuine challenge.

---

# LIN-6
**Title:** Add win/loss/draw score counter to game UI
**Body:** Track wins, losses, and draws across games in the current session and display the running score in the top corner of the game window. Should reset when the player returns to the main menu.

---

# LIN-7
**Title:** Add keyboard column selection using arrow keys and Enter
**Body:** Allow players to navigate columns using the left/right arrow keys and drop a piece with Enter, in addition to the existing mouse click controls. The preview piece should follow the selected column.

---

# LIN-8
**Title:** Add column hover highlight to improve drop target clarity
**Body:** When the player hovers over a column, highlight the entire column with a subtle overlay so it's clearer where the piece will land. Currently only the top preview piece shows, which can be hard to read.

---

# LIN-10
**Title:** Improve evaluation function threat weighting
**Body:** The current evaluation underweights blocking opponent threats. Increase the penalty for a 3-in-a-row opponent sequence from -4 to -8, and add a small bonus (+1) for single pieces with 3 open spaces to better prioritise positional play.

---

# LIN-11
**Title:** Add animated AI thinking indicator
**Body:** The current "AI is thinking" text is static. Animate it with cycling dots (e.g. "AI thinking." → "AI thinking.." → "AI thinking...") so the UI feels responsive while the AI is computing its move.

---

# LIN-12
**Title:** Add end-of-game statistics display
**Body:** After a game ends, show the total number of moves made in the game alongside the winner message. Gives players a quick summary before they restart.

---

# LIN-13
**Title:** Fix AttributeError on winning_pieces when game ends in draw
**Body:** The Board class only sets the winning_pieces attribute inside check_win(). If the game ends in a draw, draw_winning_line() in the GUI crashes with AttributeError because the attribute was never initialised. Add winning_pieces = [] to Board.__init__().

---

# LIN-14
**Title:** Fix font fallback for systems without Comic Sans MS
**Body:** The GUI hardcodes Comic Sans MS as the font. On systems where it isn't installed, pygame falls back silently to a default but the layout breaks. Use pygame.font.match_font() with a proper fallback chain so the game renders correctly on any machine.

---

# LIN-15
**Title:** Fix restart mid-game not resetting AI thinking state
**Body:** If a player resets the game mid-match while the AI is in battle mode, last_move_time and ai_start_time are not cleared. This causes the AI to fire a move immediately on the next game without waiting the configured delay. Reset these in Game.reset().

---

# LIN-16
**Title:** Rename difficulty parameter to ai_difficulty in Game constructor
**Body:** The difficulty parameter in Game.__init__() is ambiguous — it's not clear it refers to AI difficulty specifically. Rename it to ai_difficulty throughout the class and update all call sites in main.py. This is a breaking change for any external code passing difficulty as a keyword argument.

---

# LIN-17
**Title:** Add feature-flagged move hint system
**Body:** Add a ENABLE_MOVE_HINTS = False flag in game.py. When enabled, the game computes the best move for the human player at depth 3 and shows a subtle green indicator on that column. Ships disabled so it can be turned on for testing without affecting all users.

---

# LIN-18
**Title:** Refactor GUI draw methods and extract color constants
**Body:** Colors (BLUE, BLACK, RED, YELLOW, WHITE) and SQUARE_SIZE are redefined in multiple files. Extract them into src/constants.py and import from there. No behaviour change — internal cleanup to reduce duplication.
