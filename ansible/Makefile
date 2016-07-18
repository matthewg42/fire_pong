RASBIAN_IMAGE = $(HOME)/download/2016-05-27-raspbian-jessie-lite.img

.PHONY: clean burn ssh-clean

all: firepong

clean:
	rm -f burn ssh-clean expand update firepong_prep firepong *.retry

burn:
	sudo img2blockdev $(RASBIAN_IMAGE)
	touch burn

ssh-clean:
	sed -i -e '/raspberrypi/ d' ~/.ssh/known_hosts
	ssh-copy-id -i ~/.ssh/mouse_id_rsa pi@raspberrypi
	ssh pi@raspberrypi echo ssh keys added
	touch ssh-clean

expand: ssh-clean
	ansible-playbook -i inventory/firepong --sudo --user pi expand.yml
	./reboot.sh pi raspberrypi
	touch expand

update: expand
	ansible-playbook -i inventory/firepong --sudo --user pi update.yml
	./reboot.sh pi raspberrypi
	touch update

firepong_prep: update
	ansible-playbook -i inventory/firepong --sudo --user pi firepong_prep.yml
	./reboot.sh pi raspberrypi
	touch firepong_prep

firepong: firepong_prep
	ansible-playbook -i inventory/firepong --sudo --user pi firepong_install.yml
	touch firepong


