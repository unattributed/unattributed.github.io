Gem::Specification.new do |spec|
    spec.name          = "unattributed-theme"
    spec.version       = "1.0.0"
    spec.authors       = ["unattributed"]
    spec.email         = ["shopkeeper@unattributed.blog"]
    spec.summary       = "Privacy-focused Jekyll theme"
    spec.homepage      = "https://github.com/unattributed/unattributed-theme"
    spec.license       = "MIT"
    spec.files         = Dir["{_layouts,_includes,assets,_data}/**/*"] + ["LICENSE", "README.md"]
    spec.add_runtime_dependency "jekyll", ">= 3.8", "< 5.0"
    spec.add_runtime_dependency "jekyll-feed", "~> 0.15"
    spec.add_runtime_dependency "jekyll-seo-tag", "~> 2.7"
  end