CREATE TABLE inleverans (
    lev_datum          date,
    planerat_lev_datum date,
    vaccinleverantör   varchar(100),
    kvantitet_vial     int,
    gln_mottagare      varchar(100)
);

CREATE TABLE lagersaldo (
    datum_tid        date,
    vaccinleverantör varchar(100),
    kvantitet_vial   int,
    kvantitet_dos    int
);

CREATE TABLE förbrukning (
    förbrukningsdatum date,
    vaccinleverantör  varchar(100),
    kvantitet_vial    int
);

CREATE TABLE kapacitet (
    kapacitetsdatum_prognos date,
    kapacitet_doser         int
);

CREATE TABLE beställning (
    beställningsdatum date,
    önskat_lev_datum  date,
    kvantitet_dos     int,
    gln_mottagare     varchar(100)
);