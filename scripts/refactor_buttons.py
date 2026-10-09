import os

for root, dirs, files in os.walk('src'):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.ts'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content.replace(
                'import { Button } from "@/components/ui/button"',
                'import { RadialGlowButton as Button } from "@/components/ui/radial-glow-button"'
            ).replace(
                "import { Button } from '@/components/ui/button'",
                "import { RadialGlowButton as Button } from '@/components/ui/radial-glow-button'"
            )
            
            # Fix asChild in page.tsx
            if "page.tsx" in file and "asChild" in new_content:
                new_content = new_content.replace(
                    '<Button variant="ghost" size="sm" className="hidden sm:flex" asChild>\n              <Link href="/threats">\n                View All <ArrowRight className="ml-2 h-4 w-4" />\n              </Link>\n            </Button>',
                    '<Link href="/threats">\n              <Button className="hidden sm:flex">\n                View All <ArrowRight className="ml-2 h-4 w-4" />\n              </Button>\n            </Link>'
                )
            
            # Fix asChild in not-found.tsx
            if "not-found.tsx" in file and "asChild" in new_content:
                new_content = new_content.replace(
                    '<Button asChild size="lg" className="mt-4">\n        <Link href="/">\n          Return to Dashboard\n        </Link>\n      </Button>',
                    '<Link href="/">\n        <Button className="mt-4">\n          Return to Dashboard\n        </Button>\n      </Link>'
                )
            
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'Updated {path}')
