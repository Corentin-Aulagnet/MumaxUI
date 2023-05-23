from PyQt5.QtCore import QRectF, QRect, Qt ,QPoint ,QRegularExpression ,QRegularExpressionMatchIterator,QRegularExpressionMatch, QRegExp
from PyQt5.QtGui import QResizeEvent, QTextCursor, QPaintEvent, QPainter, QColor,QSyntaxHighlighter,QTextCharFormat,QFont,QTextDocument,QColor,QFont
from PyQt5.QtWidgets import QTextEdit, QApplication

from LineNumberArea import LineNumberArea
class HighlightingRule:
    def __init__(self,pattern:QRegularExpression,format:QTextCharFormat):
        self.pattern = pattern
        self.format = format

def format(color, style=''):
    """Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
    _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format
STYLES = {
       'keyword': format('blue'),
       'operator': format('red'),
       'brace': format('darkGray'),
       'string': format('magenta'),
       'string2': format('darkMagenta'),
       'comment': format('darkGreen', 'italic'),
       'numbers': format('brown'),
       'function':format('lightBrown'),
       'predefined' : format('black','italic'),
       'params' : format('blue','italic')
   }
class MumaxGoHighlighter (QSyntaxHighlighter):
        """Syntax highlighter for the Python language.
        """
        # Python keywords
        keywords = [
           'SetCellSize','SetGeom','SetGridSize','SetMesh','SetPBC','EdgeSmooth',
           'Cell','Circle','Cone','Cuboid','Cylinder','Ellipse','Ellipsoid','GrainRoughness','ImageShape','Layer','Layers','Rect','Square','Universe','XRange','YRange','ZRange',
           'DefRegion','DefRegionCell','regions',
           'AntiVortex','BlochSkyrmion','Conical','Helical','NeelSkyrmion','RandomMag','RandomMagSeed','TwoDomain','Uniform','Vortex','VortexWall',
           'AutoSave','AutoSnapshot','DUMP','FilenameFormat','Flush','Fprintln','OutputFormat','OVF1_BINARY','OVF1_TEXT','OVF2_BINARY','OVF2_TEXT','Print','Save','SaveAs','Snapshot','SnapshotAs','SnapshotFormat','sprint','sprintf','TableAdd','TableAddVar','TableAutoSave','TablePrint','TableSave',
           'Minimize','Relax','Run','RunWhile','Steps','SetSolver']
        
        matParams = ["Aex","alpha","anisC1","anisC2","anisU","B1","B2",
                     "Dbulk","Dind","EpsilonPrime","FreeLayerThickness",
                     "frozenspins","Kc1","Kc2","Kc3","Ku1","Ku2","Lambda",
                     "Msat","NoDemagSpins","Pol","Temp","xi",'m',]
        
        excitations = ['B_ext','FixedLayer','J']

        outputQuant = ['B_anis','B_custom','B_demag','B_eff','B_exch','B_mel','B_therm',
                       'DindCoupling','dt',
                       'E_anis','E_custom','E_demag','E_exch','E_mel','E_therm','E_total','E_Zeeman',
                       'Edens_anis','Edens_custom','Edens_demag','Edens_exch','Edens_mel','Edens_therm','Edens_total','Edens_Zeeman',
                       'ExchCoupling','F_mel','geom','LastErr','LLTorque','m_full','MaxAngle','maxTorque',
                       'MFM','Neval','PeakErr','spinAngle','STTTorque','torque']
        
        runParams = ['dt','FixDt','HeadRoom','LastErr','MaxDt','MaxErr','MinDt','MinimizerSamples','MinimizerStop','NEval','PeakErr','RelaxMaxTroqueThreshold','step','t',]
        # Python operators,
        operators = [
            #Initialize
            ':=',
             '=',
           # Comparison
           '==', '!=', '<', '<=', '>', '>=',
           # Arithmetic
           '\+', '-', '\*', '/', '//', '\%', '\*\*',
           # In-place
           '\+=', '-=', '\*=', '/=', '\%=',
           # Bitwise
           '\^', '\|', '\&', '\~', '>>', '<<',
        ]
  
        # Python braces
        braces = [
           '\{', '\}', '\(', '\)', '\[', '\]',
        ]
   
        def __init__(self, parent: QTextDocument) -> None:
            super().__init__(parent)
   
            # Multi-line strings (expression, flag, style)
            self.tri_single = (QRegExp("'''"), 1, STYLES['string2'])
            self.tri_double = (QRegExp('"""'), 2, STYLES['string2'])
   
            rules = []
   
            # Keyword, operator, and brace rules
            rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
               for w in MumaxGoHighlighter.keywords]
            rules += [(r'%s' % o, 0, STYLES['operator'])
               for o in MumaxGoHighlighter.operators]
            rules += [(r'%s' % b, 0, STYLES['brace'])
               for b in MumaxGoHighlighter.braces]
            
            rules += [(r'\b%s\b' % b, 0, STYLES['params'])
               for b in MumaxGoHighlighter.matParams]
            rules += [(r'\b%s\b' % b, 0, STYLES['params'])
               for b in MumaxGoHighlighter.outputQuant]
            rules += [(r'\b%s\b' % b, 0, STYLES['params'])
               for b in MumaxGoHighlighter.excitations]
   
           # All other rules
            rules += [
   
               # Numeric literals
               (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
               (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
               (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
   
              # Double-quoted string, possibly containing escape sequences
              (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
              # Single-quoted string, possibly containing escape sequences
              (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),
  
             # From '//' until a newline
                (r'//[^\n]*', 0, STYLES['comment']),
          ]
  
          # Build a QRegExp for each pattern
            self.rules = [(QRegExp(pat), index, fmt) for (pat, index, fmt) in rules]
  
        def highlightBlock(self, text):
          """Apply syntax highlighting to the given block of text.
          """
          self.tripleQuoutesWithinStrings = []
          # Do other syntax formatting
          for expression, nth, format in self.rules:
              index = expression.indexIn(text, 0)
              if index >= 0:
                  # if there is a string we check
                  # if there are some triple quotes within the string
                  # they will be ignored if they are matched again
                  if expression.pattern() in [r'"[^"\\]*(\\.[^"\\]*)*"', r"'[^'\\]*(\\.[^'\\]*)*'"]:
                      innerIndex = self.tri_single[0].indexIn(text, index + 1)
                      if innerIndex == -1:
                          innerIndex = self.tri_double[0].indexIn(text, index + 1)
  
                      if innerIndex != -1:
                          tripleQuoteIndexes = range(innerIndex, innerIndex + 3)
                          self.tripleQuoutesWithinStrings.extend(tripleQuoteIndexes)
  
              while index >= 0:
                  # skipping triple quotes within strings
                  if index in self.tripleQuoutesWithinStrings:
                      index += 1
                      expression.indexIn(text, index)
                      continue
  
                  # We actually want the index of the nth match
                  index = expression.pos(nth)
                  length = len(expression.cap(nth))
                  self.setFormat(index, length, format)
                  index = expression.indexIn(text, index + length)
  
          self.setCurrentBlockState(0)
  
          # Do multi-line strings
          in_multiline = self.match_multiline(text, *self.tri_single)
          if not in_multiline:
              in_multiline = self.match_multiline(text, *self.tri_double)
  
        def match_multiline(self, text, delimiter, in_state, style):
          """Do highlighting of multi-line strings. ``delimiter`` should be a
          ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
          ``in_state`` should be a unique integer to represent the corresponding
          state changes when inside those strings. Returns True if we're still
          inside a multi-line string when this function is finished.
          """
          # If inside triple-single quotes, start at 0
          if self.previousBlockState() == in_state:
              start = 0
              add = 0
          # Otherwise, look for the delimiter on this line
          else:
              start = delimiter.indexIn(text)
              # skipping triple quotes within strings
              if start in self.tripleQuoutesWithinStrings:
                  return False
              # Move past this match
              add = delimiter.matchedLength()
  
          # As long as there's a delimiter match on this line...
          while start >= 0:
              # Look for the ending delimiter
              end = delimiter.indexIn(text, start + add)
              # Ending delimiter on this line?
              if end >= add:
                  length = end - start + add + delimiter.matchedLength()
                  self.setCurrentBlockState(0)
              # No; multi-line string
              else:
                  self.setCurrentBlockState(in_state)
                  length = len(text) - start + add
              # Apply formatting
              self.setFormat(start, length, style)
              # Look for the next match
              start = delimiter.indexIn(text, start + length)
  
          # Return True if still inside a multi-line string, False otherwise
          if self.currentBlockState() == in_state:
             return True
          else:
              return False
class QTextEditHighlighter(QTextEdit):
    def __init__(self):
        # Line numbers
        QTextEdit.__init__(self)
        self.lineNumberArea = LineNumberArea(self)

        self.document().blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.verticalScrollBar().valueChanged.connect(self.updateLineNumberArea)
        self.textChanged.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.updateLineNumberArea)

        self.updateLineNumberAreaWidth(0)
        

    def lineNumberAreaWidth(self):
        digits = 1
        m = max(1, self.document().blockCount())
        while m >= 10:
            m /= 10
            digits += 1
        space = 13 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, newBlockCount: int):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberAreaRect(self, rect_f: QRectF):
        self.updateLineNumberArea()

    def updateLineNumberAreaInt(self, slider_pos: int):
        self.updateLineNumberArea()

    def updateLineNumberArea(self):
        """        
        When the signal is emitted, the sliderPosition has been adjusted according to the action,
        but the value has not yet been propagated (meaning the valueChanged() signal was not yet emitted),
        and the visual display has not been updated. In slots connected to self signal you can thus safely
        adjust any action by calling setSliderPosition() yourself, based on both the action and the
        slider's value.
        """
        
        # Make sure the sliderPosition triggers one last time the valueChanged() signal with the actual value !!!!
        self.verticalScrollBar().setSliderPosition(self.verticalScrollBar().sliderPosition())
    
        # Since "QTextEdit" does not have an "updateRequest(...)" signal, we chose
        # to grab the imformations from "sliderPosition()" and "contentsRect()".
        # See the necessary connections used (Class constructor implementation part).
    
        rect = self.contentsRect()

        self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        self.updateLineNumberAreaWidth(0)
        
        dy = self.verticalScrollBar().sliderPosition()
        if dy > -1:
            self.lineNumberArea.scroll(0, dy)
    
        # Addjust slider to alway see the number of the currently being edited line...
        first_block_id = self.getFirstVisibleBlockId()
        if first_block_id == 0 or self.textCursor().block().blockNumber() == first_block_id-1:
            self.verticalScrollBar().setSliderPosition(int(dy-self.document().documentMargin()))
    
    #    # Snap to first line (TODO...)
    #    if first_block_id > 0:
    #        slider_pos = self.verticalScrollBar().sliderPosition()
    #        prev_block_height = (int) self.document().documentLayout().blockBoundingRect(self.document().findBlockByNumber(first_block_id-1)).height()
    #        if (dy <= self.document().documentMargin() + prev_block_height)
    #            self.verticalScrollBar().setSliderPosition(slider_pos - (self.document().documentMargin() + prev_block_height))

    def resizeEvent(self, event: QResizeEvent):
        QTextEdit.resizeEvent(self, event)

        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def getFirstVisibleBlockId(self) -> int:
        # Detect the first block for which bounding rect - once translated
        # in absolute coordinated - is contained by the editor's text area
    
        # Costly way of doing but since "blockBoundingGeometry(...)" doesn't
        # exists for "QTextEdit"...
    
        curs = QTextCursor(self.document())
        curs.movePosition(QTextCursor.Start)
        for i in range(self.document().blockCount()):
            block = curs.block()
    
            r1 = self.viewport().geometry()
            r2 = self.document().documentLayout().blockBoundingRect(block).translated(
                    self.viewport().geometry().x(), self.viewport().geometry().y() - (
                        self.verticalScrollBar().sliderPosition()
                        )).toRect()
    
            if r1.contains(r2, True):
                return i
    
            curs.movePosition(QTextCursor.NextBlock)
        return 0
    
    def lineNumberAreaPaintEvent(self, event: QPaintEvent):
        self.verticalScrollBar().setSliderPosition(self.verticalScrollBar().sliderPosition())
    
        painter = QPainter(self.lineNumberArea)
        #Draw the area where numbers are displayed
        col_1 = QColor(15, 20, 166 )      # Current line (custom green)
        col_0 = QColor(120, 120, 120)    # Other lines  (custom darkgrey)

        painter.fillRect(event.rect(), Qt.white)
        painter.drawLine(QPoint(event.rect().right(),event.rect().top()),QPoint(event.rect().right(),event.rect().bottom()))
        blockNumber = self.getFirstVisibleBlockId()
    
        block = self.document().findBlockByNumber(blockNumber)

        if blockNumber > 0:
            prev_block = self.document().findBlockByNumber(blockNumber - 1)
        else:
            prev_block = block

        if blockNumber > 0:
            translate_y = -self.verticalScrollBar().sliderPosition()
        else:
            translate_y = 0
    
        top = self.viewport().geometry().top()
    
        # Adjust text position according to the previous "non entirely visible" block
        # if applicable. Also takes in consideration the document's margin offset.

        if blockNumber == 0:
            # Simply adjust to document's margin
            additional_margin = self.document().documentMargin() -1 - self.verticalScrollBar().sliderPosition()
        else:
            # Getting the height of the visible part of the previous "non entirely visible" block
            additional_margin = self.document().documentLayout().blockBoundingRect(prev_block) \
                    .translated(0, translate_y).intersected(QRectF(self.viewport().geometry())).height()
    
        # Shift the starting point
        top += additional_margin
    
        bottom = top + int(self.document().documentLayout().blockBoundingRect(block).height())
    
       
        # Draw the numbers (displaying the current line number in green)
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = f"{blockNumber + 1}"
                painter.setPen(col_0)

                if self.textCursor().blockNumber() == blockNumber:
                    painter.setPen(col_1)
                else:
                    painter.setPen(col_0)

                painter.drawText(-5, int(top),
                                 int(self.lineNumberArea.width()), int(self.fontMetrics().height()),
                                 Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + int(self.document().documentLayout().blockBoundingRect(block).height())
            blockNumber += 1


if __name__ == '__main__':
    app = QApplication([])
    w = QTextEditHighlighter()
    w.show()
    app.exec()