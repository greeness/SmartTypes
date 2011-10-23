
CREATE FUNCTION ts_modifieddate() RETURNS trigger
AS $$
BEGIN
    NEW.modifieddate = now();
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;        
        
        
create table twitter_user(
    createddate timestamp not null default now(),
    modifieddate timestamp not null default now(),
    twitter_id integer unique not null,
    screen_name text not null,
    twitter_account_created timestamp,
    favourites_count integer,
    protected boolean,
    following_count integer,
    location_name text,
    description text,
    url text,
    last_loaded_following_ids timestamp default '2000-1-1',
    following_ids integer[],
    caused_an_error timestamp
);

CREATE TRIGGER twitter_user_modified BEFORE UPDATE
ON twitter_user FOR EACH ROW
EXECUTE PROCEDURE ts_modifieddate();


