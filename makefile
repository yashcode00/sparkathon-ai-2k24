.PHONY: run clean init update_requirements

run: app.py
	@echo "Starting Flask application..."
	@python3 app.py

clean:
	@echo "Cleaning up temporary files..."
	@rm -rf __pycache__ uploads

init:
	@echo "Initializing project..."
	@pip install -r requirements.txt

update_requirements:
	@echo "Updating requirements.txt..."
	@pip freeze > requirements.txt
	@echo "Requirements updated."
