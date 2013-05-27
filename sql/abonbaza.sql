CREATE INDEX abonbaza_address_my
  ON abonbaza
  USING btree
  (upper(ul) varchar_pattern_ops, upper(nd), upper(nkor), upper(nkw));

CREATE INDEX abonbaza_fio_my
  ON abonbaza
  USING btree
  (upper(fio) varchar_pattern_ops);
