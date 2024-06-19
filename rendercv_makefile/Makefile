create:
	rendercv new "Name"  # TODO: use my name but create autobackup of existing files

render:  # Includes my email and phone number
	rendercv render Bert_de_Bruijn_CV.yaml
	cp output/Bert_de_Bruijn_CV.pdf output/complete/Bert_de_Bruijn_CV.pdf

render_no_mail_phone:  # Version without email and phone number
	cp Bert_de_Bruijn_CV.yaml Bert_de_Bruijn_CV_without_email_phone.yaml
	sed -i 's/email: .*.com//' Bert_de_Bruijn_CV_without_email_phone.yaml
	sed -i 's/phone: tel:+.*//' Bert_de_Bruijn_CV_without_email_phone.yaml
	rendercv render Bert_de_Bruijn_CV_without_email_phone.yaml
	cp output/Bert_de_Bruijn_CV.pdf output/no_phone_mail/Bert_de_Bruijn_CV.pdf
	rm Bert_de_Bruijn_CV_without_email_phone.yaml

render_no_phone:  # Version without phone number
	cp Bert_de_Bruijn_CV.yaml Bert_de_Bruijn_CV_without_phone.yaml
	sed -i 's/phone: tel:+.*//' Bert_de_Bruijn_CV_without_phone.yaml
	rendercv render Bert_de_Bruijn_CV_without_phone.yaml
	cp output/Bert_de_Bruijn_CV.pdf output/no_phone/Bert_de_Bruijn_CV.pdf
	rm Bert_de_Bruijn_CV_without_phone.yaml

render_all: render render_no_mail_phone render_no_phone

push_to_random_stuff_repository:  # Make this Makefile available in my random stuff repo
	cp Makefile ~/Coding/git_personal/random/rendercv_makefile/
	cp output/no_phone_mail/Bert_de_Bruijn_CV.pdf ~/Coding/git_personal/random/rendercv_makefile/