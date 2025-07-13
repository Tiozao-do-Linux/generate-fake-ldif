
# Create virtualenvironment
python -m venv .venv
. .venv/bin/activate

# Install dependencies
pip install faker unidecode


# Build docker image
docker build -t jarbelix/generate-fake-ldif .

# Run docker container with ARG
docker run --rm -it --name generate-fake-ldif jarbelix/generate-fake-ldif 1 > /tmp/fake.ldif