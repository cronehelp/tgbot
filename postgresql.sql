PGDMP     ,    $                |            postgres    14.11 (Homebrew)    14.11 (Homebrew)     ?           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            @           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            A           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            B           1262    14088    postgres    DATABASE     S   CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'C';
    DROP DATABASE postgres;
                ivan    false            C           0    0    DATABASE postgres    COMMENT     N   COMMENT ON DATABASE postgres IS 'default administrative connection database';
                   ivan    false    3650            �            1259    16385    users    TABLE     �   CREATE TABLE public.users (
    id integer NOT NULL,
    telegram_id bigint NOT NULL,
    achievements text[],
    audio_codes text[],
    best_score integer DEFAULT 0
);
    DROP TABLE public.users;
       public         heap    ivan    false            �            1259    16384    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public          ivan    false    210            D           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public          ivan    false    209            �           2604    16388    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          ivan    false    210    209    210            <          0    16385    users 
   TABLE DATA           W   COPY public.users (id, telegram_id, achievements, audio_codes, best_score) FROM stdin;
    public          ivan    false    210   p       E           0    0    users_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.users_id_seq', 21, true);
          public          ivan    false    209            �           2606    16392    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            ivan    false    210            �           2606    16394    users users_telegram_id_key 
   CONSTRAINT     ]   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_telegram_id_key UNIQUE (telegram_id);
 E   ALTER TABLE ONLY public.users DROP CONSTRAINT users_telegram_id_key;
       public            ivan    false    210            <   ?   x�3�44�066071�NL��L-K�M�+1�rKS2�.CNc33ssKC���b���� �wZ     