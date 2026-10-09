import os

for root, dirs, files in os.walk('src'):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.ts'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content.replace(
                'import { RadialGlowButton as Button } from "@/components/ui/radial-glow-button"',
                'import { Button } from "@/components/ui/button"'
            ).replace(
                "import { RadialGlowButton as Button } from '@/components/ui/radial-glow-button'",
                "import { Button } from '@/components/ui/button'"
            )
            
            if "page.tsx" in file and 'Button className="hidden sm:flex"' in new_content:
                new_content = new_content.replace(
                    '<Link href="/threats">\n              <Button className="hidden sm:flex">\n                View All <ArrowRight className="ml-2 h-4 w-4" />\n              </Button>\n            </Link>',
                    '<Button variant="ghost" size="sm" className="hidden sm:flex" asChild>\n              <Link href="/threats">\n                View All <ArrowRight className="ml-2 h-4 w-4" />\n              </Link>\n            </Button>'
                )
            
            if "not-found.tsx" in file and 'Button className="mt-4"' in new_content:
                new_content = new_content.replace(
                    '<Link href="/">\n        <Button className="mt-4">\n          Return to Dashboard\n        </Button>\n      </Link>',
                    '<Button asChild size="lg" className="mt-4">\n        <Link href="/">\n          Return to Dashboard\n        </Link>\n      </Button>'
                )
            
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'Reverted {path}')
