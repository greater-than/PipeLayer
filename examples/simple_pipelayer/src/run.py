from app.app import main
from app.render import print_manifest, print_output

pipeline, output = main()

print_manifest(pipeline.manifest)
print_output(output)
