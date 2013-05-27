CREATE INDEX auth_user_email_my
  ON auth_user
  USING btree
  (upper(email));
