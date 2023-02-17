
import os
import sys
import yaml

def write_localization_file(language, strings, filepath, written_keys, fallback_lang=None):
    def read_key(language, key, dict, nested_key, file_contents, written_keys, original_locale=None):
        if isinstance(dict[key], str):
            if key == language:
                if not nested_key in written_keys:
                    if not original_locale is None:
                        print('(%s) missing key "%s"' % (original_locale, nested_key))
                    written_keys.add(nested_key)
                    file_contents.append('"' + nested_key + '"' + ' = ' + '"' + dict[key] + '";')
        else:
            for next_key in dict[key].keys():
                if next_key == language:
                    if not nested_key in written_keys:
                        if not original_locale is None:
                            print('(%s) missing key "%s"' % (original_locale, nested_key))
                        written_keys.add(nested_key)
                        file_contents.append('"' + nested_key + '"' + ' = ' + '"' + dict[key][next_key] + '";')
                else:
                    read_key(language, next_key, dict[key], nested_key + '.' + next_key, file_contents, written_keys, original_locale)

    file_contents = []
    for key in strings.keys():
        read_key(language, key, strings, key, file_contents, written_keys)

    if not fallback_lang is None:
        for key in strings.keys():
            read_key(fallback_lang, key, strings, key, file_contents, written_keys, language)

    try:
        os.makedirs(filepath)
    except:
        pass

    with open(os.path.join(filepath, 'Localizable.strings'), 'w') as file:
        file.write('\n'.join(file_contents))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage: localize.py <path to keys.yaml> <output_dir(s)>...')
        exit(1)

    keys_file = sys.argv[1]
    output_dirs = sys.argv[2:]

    with open(keys_file, 'r') as file:
        strings = yaml.safe_load(file.read())

        localizations = [('en', None), ('de', 'en')]
        for (locale, fallback) in localizations:

            for output_dir in output_dirs:
                written_keys = set()
                write_localization_file(locale, strings,
                    '%s/%s.lproj' % (output_dir, locale), written_keys, fallback_lang=fallback)
            
                print('wrote %d keys for %s localization' % (len(written_keys), locale))