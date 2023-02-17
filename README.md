# Localize It

LocalizeIt is a utility script for Localization in Swift Apps. It allows you to define your app's localization keys in a single YAML file for all supported languages instead of several `.strings` files.

## Installation

LocalizeIt has a single requirement, [PyYAML](https://pypi.org/project/PyYAML/). The installation example creates a virtual environment for managing this dependency.

```bash
# Clone this repository
git clone https://github.com/jonaszell97/LocalizeIt.git
cd LegalizeIt

# Create virtual env and install dependencies
python -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

## Usage

To use the script, you need to provide the path to the YAML file containing your localizations as well as one or more output directories.

Key names are determined by the hierarchy of your YAML file. Nested keys are separated with `.` in the final localization key, and the last layer in the YAML hierarchy represents the language name.

For example, take the following YAML file:

```YAML
# keys.yaml
app:
  ui:
    accept:
      en: Accept
      de: Akzeptieren
    cancel:
      en: Cancel
      de: Abbrechen
```

Running it would produce the following `.strings` files based on this definition:

```swift
// <output_dir>/en.proj/Localizable.strings
"app.ui.accept" = "Accept";
"app.ui.cancel" = "Cancel";
```

```swift
// <output_dir>/de.proj/Localizable.strings
"app.ui.accept" = "Akzeptieren";
"app.ui.cancel" = "Abbrechen";
```

You can then use these localization keys in your app.

```swift
Text("app.ui.accept") // -> "Accept"
```

LegalizeIt will output a file called `Localizable.strings` in `.lproj` subdirectories within the output directory.

As an example, if you support the languages `en` and `de`, calling the script will write the files `<output_dir>/en.lproj/Localizable.strings` and `<output_dir>/de.lproj/Localizable.strings` for every `output_dir`.

```bash
# Run the script
python src/localize.py <path to keys.yaml> <output_dir(s)>...
```