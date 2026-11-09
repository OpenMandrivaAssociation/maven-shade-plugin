%bcond_with javadoc
Name:           maven-shade-plugin
Version:        3.6.2
Release:        2
Summary:        This plugin provides the capability to package the artifact in an uber-jar
Group:          Development/Java
License:        ASL 2.0
URL:            https://maven.apache.org/plugins/%{name}
Source0:        https://github.com/apache/maven-shade-plugin/archive/refs/tags/maven-shade-plugin-%{version}.tar.gz
BuildArch:      noarch
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven

BuildRequires:  maven-plugins-pom
BuildRequires:  maven-components
BuildRequires:	mvn(com.google.inject:guice-parent:pom::)
BuildRequires:	mvn(org.slf4j:slf4j-parent:pom::)
BuildRequires:	mvn(org.codehaus.plexus:plexus-containers:pom::)
BuildRequires:  mvn(org.ow2.asm:asm) >= 9
BuildRequires:  mvn(org.ow2.asm:asm-commons) >= 9
BuildRequires:  mvn(org.jdom:jdom2)
BuildRequires:  jdependency >= 2.17
BuildRequires:  plexus-utils >= 3.6.0

Obsoletes:      maven2-plugin-shade <= 0:2.0.8
Provides:       maven2-plugin-shade = 1:%{version}-%{release}

%description
This plugin provides the capability to package the artifact in an
uber-jar, including its dependencies and to shade - i.e. rename - the
packages of some of the dependencies.


%if %{with javadoc}
%package javadoc
Summary:        API documentation for %{name}

%endif
%if %{with javadoc}
%description javadoc
%{summary}.

%endif
%prep
%setup -q -n maven-shade-plugin-maven-shade-plugin-%{version}
# JUnit and Hamcrest are not imported. Upstream marked the first copy compile.
python - <<'PY'
import xml.etree.ElementTree as ET
NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def local(tag):
    return tag.split("}", 1)[-1]

tree = ET.parse("pom.xml")
root = tree.getroot()
drop = {"junit", "hamcrest", "hamcrest-core"}
for deps in list(root.iter()):
    if local(deps.tag) != "dependencies":
        continue
    for dep in list(deps):
        artifact = ""
        scope = ""
        for node in dep:
            name = local(node.tag)
            if name == "artifactId":
                artifact = (node.text or "").strip()
            elif name == "scope":
                scope = (node.text or "").strip()
        if artifact in drop and scope != "test":
            deps.remove(dep)
tree.write("pom.xml", encoding="utf-8", xml_declaration=True)
PY
# ShadeMojo injects Shader by @Named. The published jar had the annotation
# and no sisu index, so the component was null.
python - <<'PY'
import re
from pathlib import Path

def named_in(root):
    names = []
    for path in sorted(Path(root).rglob("*.java")):
        text = path.read_text(encoding="utf-8", errors="replace")
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
        text = re.sub(r"//.*?$", "", text, flags=re.M)
        match = re.search(r"\b(?:class|interface|enum)\s+([A-Za-z0-9_]+)", text)
        if not match or "@Named" not in text[:match.start()]:
            continue
        pkg = re.search(r"(?m)^package\s+([A-Za-z0-9_.]+)\s*;", text)
        if pkg:
            names.append(pkg.group(1) + "." + match.group(1))
    return names

names = named_in("src/main/java")
if names != ["org.apache.maven.plugins.shade.DefaultShader"]:
    raise SystemExit("expected DefaultShader, got " + str(names))
dest = Path("src/main/resources/META-INF/sisu")
dest.mkdir(parents=True, exist_ok=True)
(dest / "javax.inject.Named").write_text("\n".join(names) + "\n", encoding="utf-8")
PY

%files -f .mfiles
%doc LICENSE README.md

%if %{with javadoc}
%files javadoc -f .mfiles-javadoc
%doc LICENSE README.md

%endif
