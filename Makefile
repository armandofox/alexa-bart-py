AWS = aws
ZIP = zip
PYTHON = python

SKILL_NAME = pogoBart
ZIPFILE = _$(SKILL_NAME).zip

zip: $(ZIPFILE)

$(ZIPFILE): $(wildcard lambda/*)
	cd lambda && $(ZIP) -q -X -r ../$(ZIPFILE) *

upload_lambda: $(ZIPFILE)
	$(AWS) lambda update-function-code --function-name $(SKILL_NAME) --zip-file fileb://$(ZIPFILE)

skill/utterances.txt: skill/utterances.txt.glob
	$(PYTHON) lambda/ask/unglob_intent.py $< > $@
