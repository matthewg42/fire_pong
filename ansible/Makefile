RASBIAN_IMAGE = $(HOME)/download/2016-05-27-raspbian-jessie-lite.img

.PHONY: clean burn ssh-clean

clean:
	rm -f burn expand update firepong *.retry

burn:
	sudo img2blockdev $(RASBIAN_IMAGE)
	touch burn

ssh-clean:
	sed -i -e '/raspberrypi/ d' ~/.ssh/known_hosts
	ssh-copy-id -i ~/.ssh/mouse_id_rsa pi@raspberrypi
	ssh pi@raspberrypi echo ssh keys added

expand: ssh-clean
	ansible-playbook -i inventory/firepong --sudo --user pi expand.yml
	./reboot.sh pi raspberrypi
	touch expand

update: ssh-clean expand
	ansible-playbook -i inventory/firepong --sudo --user pi update.yml
	./reboot.sh pi raspberrypi
	touch update

firepong: ssh-clean update
	ansible-playbook -i inventory/firepong --sudo --user pi firepong.yml
	./reboot.sh pi raspberrypi
	touch firepong


