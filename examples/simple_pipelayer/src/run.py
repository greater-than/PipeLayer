from app.app import main
from app.render import print_manifest, print_output

manifest, output = main()

print_manifest(manifest)
print_output(output)
