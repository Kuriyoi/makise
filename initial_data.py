from src.database.models import User, Address, Manga, Wishlist, Supplier, Review, Payment, Order, OrderManga, New
from datetime import datetime, timedelta


def add_initial_data():
    user_1 = User('admin@example.com', 'admin', 'Admin', 'Admin Admin', '666666666', True)
    user_2 = User('user1@example.com', 'user1', 'Antonio', 'Rivera Molina', '612345678', False)
    user_3 = User('user2@example.com', 'user2', 'Carmen', 'Moriana Romero', '623456789', False)
    user_4 = User('user3@example.com', 'user3', 'Antonia', 'Romero Moriana', '634567891', False)
    user_5 = User('user4@example.com', 'user4', 'Manuel', 'Molina Rivera', '645678912', False)
    user_6 = User('user5@example.com', 'user5', 'Manuela', 'Castilero Alba', '656789123', False)
    user_7 = User('user6@example.com', 'user6', 'Francisco', 'Alba Castillero', '667891234', False)
    user_8 = User('user7@example.com', 'user7', 'Laura', 'de Luque Alfonso', '678912345', False)
    user_9 = User('user8@example.com', 'user8', 'Juan', 'Alfonso de Luque', '689123456', False)
    user_10 = User('user9@example.com', 'user9', 'Daniel', 'Molina Alfonso', '691234567', False)
    user_11 = User('user10@example.com', 'user10', 'Isabel', 'Castillero Rivera', '698765432', False)
    user_12 = User('user11@example.com', 'user11', 'Josefa', 'Molina Romero', '687654321', False)

    address_1 = Address('Casa', 'Calle Larga 2', 'Sevilla', 'Sevilla', '12345', user_1.id_user)
    address_2 = Address('Hogar', 'Calle Corta 23', 'Camas', 'Sevilla', '54321', user_2.id_user)
    address_3 = Address('Dir 1', 'Avenida de la Hoja 3', 'Huelva', 'Huelva', '12457', user_3.id_user)
    address_4 = Address('Casa 1', 'Calle Mitad 45', 'Granada', 'Granada', '12369', user_4.id_user)
    address_5 = Address('Playa', 'Calle Delicada 67', 'Madrid', 'Madrid', '12356', user_5.id_user)
    address_6 = Address('Casa', 'Avenida Estrecha 78', 'Alicante', 'Alicante', '23568', user_6.id_user)
    address_7 = Address('Casa', 'Calle Agua 34', 'Zaragoza', 'Zaragoza', '56328', user_7.id_user)
    address_8 = Address('Trabajo', 'Calle Fuego 56', 'Segovia', 'Segovia', '56478', user_8.id_user)
    address_9 = Address('Oficina', 'Avenida Locura 98', 'Guadarrama', 'Madrid', '46985', user_9.id_user)
    address_10 = Address('Tienda', 'Calle Tranquila 104', 'Valencia', 'Valencia', '35687', user_10.id_user)
    address_11 = Address('Casa', 'Calle Abandonada 90', 'Barcelona', 'Barcelona', '42135', user_11.id_user)
    address_12 = Address('Casa', 'Avenida Kurisu 004', 'Alpedrete', 'Madrid', '28430', user_12.id_user)

    user_1.addresses_user.append(address_1)
    user_2.addresses_user.append(address_2)
    user_3.addresses_user.append(address_3)
    user_4.addresses_user.append(address_4)
    user_5.addresses_user.append(address_5)
    user_6.addresses_user.append(address_6)
    user_7.addresses_user.append(address_7)
    user_8.addresses_user.append(address_8)
    user_9.addresses_user.append(address_9)
    user_10.addresses_user.append(address_10)
    user_11.addresses_user.append(address_11)
    user_12.addresses_user.append(address_12)

    supplier_1 = Supplier('Distriforma', '916845570', 'distriforma@distriforma.es')
    supplier_2 = Supplier('Azeta Distribuciones', '958552085', 'info@azeta.es')
    supplier_3 = Supplier('SD Distribuciones', '933001022', 'info@sddistribuciones.com')

    manga_1 = Manga('Ayashimon 1', 'Yuji Kaku', 'Maruo, un chico rebelde de fuerza extraordinaria, se adentra en el mundo de la mafia dirigido por los ayashimon junto a Urara, su reclutadora, la hija del difunto líder del clan Enma. Su destino es el barrio de Kabukichô en Shinjuku, donde todo se decide con lances.', 9, 100, 'ayashimon_1.png', 'Acción', 'Norma Editorial', datetime.now() - timedelta(weeks=2, hours=12), supplier_1.id_supplier)
    manga_2 = Manga('Oshi no Ko 5', 'Aka Akasaka', 'Ai Hoshino es una popular idol de 16 años que lo tiene todo para triunfar: una imagen bella e inocente y talento. Aunque no todo es tan bonito como lo pintan… Un día, Ai se presenta en la consulta de Goro Honda, un ginecólogo que es un gran fan suyo, pero trae una sorpresa: está embarazada de gemelos. Poco puede imaginar Goro que acabará muerto… ¡para renacer como Aquamarine Hoshino, uno de los hijos recién nacidos de Ai! Un mundo que no es de color de rosa como imaginaba, en el que las puñaladas por la espalda y la competitividad enfermiza están a la orden del día. Y por si fuera poco la relación entre los gemelos y su madre revelará más de una sorpresa que nos dejará alucinados.', 8.50, 23, 'oshi_no_ko_5.png', 'Drama', 'Editorial Ivrea', datetime.now() - timedelta(weeks=2, hours=12), supplier_2.id_supplier)
    manga_3 = Manga('Oshi no Ko 6', 'Aka Akasaka', 'Ai Hoshino es una popular idol de 16 años que lo tiene todo para triunfar: una imagen bella e inocente y talento. Aunque no todo es tan bonito como lo pintan… Un día, Ai se presenta en la consulta de Goro Honda, un ginecólogo que es un gran fan suyo, pero trae una sorpresa: está embarazada de gemelos. Poco puede imaginar Goro que acabará muerto… ¡para renacer como Aquamarine Hoshino, uno de los hijos recién nacidos de Ai! Un mundo que no es de color de rosa como imaginaba, en el que las puñaladas por la espalda y la competitividad enfermiza están a la orden del día. Y por si fuera poco la relación entre los gemelos y su madre revelará más de una sorpresa que nos dejará alucinados.', 8.50, 34, 'oshi_no_ko_6.png', 'Drama', 'Editorial Ivrea', datetime.now() - timedelta(weeks=2, hours=12), supplier_2.id_supplier)
    manga_4 = Manga('Oshi no Ko 7', 'Aka Akasaka', 'Ai Hoshino es una popular idol de 16 años que lo tiene todo para triunfar: una imagen bella e inocente y talento. Aunque no todo es tan bonito como lo pintan… Un día, Ai se presenta en la consulta de Goro Honda, un ginecólogo que es un gran fan suyo, pero trae una sorpresa: está embarazada de gemelos. Poco puede imaginar Goro que acabará muerto… ¡para renacer como Aquamarine Hoshino, uno de los hijos recién nacidos de Ai! Un mundo que no es de color de rosa como imaginaba, en el que las puñaladas por la espalda y la competitividad enfermiza están a la orden del día. Y por si fuera poco la relación entre los gemelos y su madre revelará más de una sorpresa que nos dejará alucinados.', 8.50, 36, 'oshi_no_ko_7.png', 'Drama', 'Editorial Ivrea', datetime.now() - timedelta(weeks=2, hours=12), supplier_2.id_supplier)
    manga_5 = Manga('Oshi no Ko 8', 'Aka Akasaka', 'Ai Hoshino es una popular idol de 16 años que lo tiene todo para triunfar: una imagen bella e inocente y talento. Aunque no todo es tan bonito como lo pintan… Un día, Ai se presenta en la consulta de Goro Honda, un ginecólogo que es un gran fan suyo, pero trae una sorpresa: está embarazada de gemelos. Poco puede imaginar Goro que acabará muerto… ¡para renacer como Aquamarine Hoshino, uno de los hijos recién nacidos de Ai! Un mundo que no es de color de rosa como imaginaba, en el que las puñaladas por la espalda y la competitividad enfermiza están a la orden del día. Y por si fuera poco la relación entre los gemelos y su madre revelará más de una sorpresa que nos dejará alucinados.', 8.50, 42, 'oshi_no_ko_8.png', 'Drama', 'Editorial Ivrea', datetime.now() - timedelta(weeks=2, hours=12), supplier_2.id_supplier)
    manga_6 = Manga('Oshi no Ko 9', 'Aka Akasaka', 'Ai Hoshino es una popular idol de 16 años que lo tiene todo para triunfar: una imagen bella e inocente y talento. Aunque no todo es tan bonito como lo pintan… Un día, Ai se presenta en la consulta de Goro Honda, un ginecólogo que es un gran fan suyo, pero trae una sorpresa: está embarazada de gemelos. Poco puede imaginar Goro que acabará muerto… ¡para renacer como Aquamarine Hoshino, uno de los hijos recién nacidos de Ai! Un mundo que no es de color de rosa como imaginaba, en el que las puñaladas por la espalda y la competitividad enfermiza están a la orden del día. Y por si fuera poco la relación entre los gemelos y su madre revelará más de una sorpresa que nos dejará alucinados.', 8.50, 45, 'oshi_no_ko_9.png', 'Drama', 'Editorial Ivrea', datetime.now() - timedelta(weeks=2, hours=12), supplier_2.id_supplier)
    manga_7 = Manga('Oshi no Ko 10', 'Aka Akasaka', 'Ai Hoshino es una popular idol de 16 años que lo tiene todo para triunfar: una imagen bella e inocente y talento. Aunque no todo es tan bonito como lo pintan… Un día, Ai se presenta en la consulta de Goro Honda, un ginecólogo que es un gran fan suyo, pero trae una sorpresa: está embarazada de gemelos. Poco puede imaginar Goro que acabará muerto… ¡para renacer como Aquamarine Hoshino, uno de los hijos recién nacidos de Ai! Un mundo que no es de color de rosa como imaginaba, en el que las puñaladas por la espalda y la competitividad enfermiza están a la orden del día. Y por si fuera poco la relación entre los gemelos y su madre revelará más de una sorpresa que nos dejará alucinados.', 8.50, 57, 'oshi_no_ko_10.png', 'Drama', 'Editorial Ivrea', datetime.now() - timedelta(weeks=2, hours=12), supplier_2.id_supplier)
    manga_8 = Manga('Oshi no Ko 11', 'Aka Akasaka', 'Ai Hoshino es una popular idol de 16 años que lo tiene todo para triunfar: una imagen bella e inocente y talento. Aunque no todo es tan bonito como lo pintan… Un día, Ai se presenta en la consulta de Goro Honda, un ginecólogo que es un gran fan suyo, pero trae una sorpresa: está embarazada de gemelos. Poco puede imaginar Goro que acabará muerto… ¡para renacer como Aquamarine Hoshino, uno de los hijos recién nacidos de Ai! Un mundo que no es de color de rosa como imaginaba, en el que las puñaladas por la espalda y la competitividad enfermiza están a la orden del día. Y por si fuera poco la relación entre los gemelos y su madre revelará más de una sorpresa que nos dejará alucinados.', 8.50, 60, 'oshi_no_ko_11.png', 'Drama', 'Editorial Ivrea', datetime.now() - timedelta(weeks=2, hours=12), supplier_2.id_supplier)
    manga_9 = Manga('Spy x Family 12', 'Tatsuya Endo', 'Los países de Westalis y Ostania libran desde hace años una guerra fría donde el espionaje y los asesinatos son moneda corriente. El inigualable espía conocido como "Twilight" es el mejor agente de Westalis que tiene por objetivo encargarse del poderoso Donovan Desmond. La putada es que Desmond es un ermitaño antisocial cuyas únicas apariciones públicas son en los actos escolares de su hijo. Twilight deberá acercarse al objetivo lo suficiente como para desbaratar su agenda secreta. Para ello, sólo deberá simular que es un hombre de familia... con el pequeño detalle de que sólo tiene 7 días para conseguir la familia ideal. Es por eso que bajo la identidad del psiquiatra Loid Forger, Twilight reclutará a Yor Briar, una civil ostaniana que quiere tener bajo perfil y Anya, una huerfanita que sólo busca una familia cariñosa, para hacer las partes de esposa e hija respectivamente. Pero resulta que este par tampoco es nada normal, especialmente si tenemos en cuenta que Yor es una asesina profesional buscada por ambos bandos y Anya es una prófuga de un laboratorio secreto donde consiguió poderes telepáticos. La típica familia normal diréis…. Si cuela, cuela… Es así como los tres se sentirán como un pulpo en un garaje y a la vez deberán cumplir con sus respectivos objetivos, por obligación o por deseo, mientras intentan llevar una vida cotidiana lo más normal que les permita sus situaciones.', 8.50, 75, 'spy_family_12.png', 'Comedia', 'Editorial Ivrea', datetime.now() - timedelta(weeks=2, hours=12), supplier_2.id_supplier)
    manga_10 = Manga('Neon Genesis Evangelion 4', 'Yoshiyuki Sadamoto', 'Vuelve Neon Genesis Evangelion, uno de los mangas de culto más populares, pero esta vez lo hace en una fantástica edición coleccionista que los fans de la serie no podrán dejar escapar. Esta revolucionaria saga que marcó un antes y un después en su género mezcla ciencia ficción con un diseccionado análisis del alma humana que no deja indiferente a sus lectores...', 14.95, 12, 'neon_genesis_evangelion_col_4.png', 'Sci-Fi', 'Norma Editorial', datetime.now() - timedelta(weeks=2, hours=12), supplier_1.id_supplier)
    manga_11 = Manga('Neon Genesis Evangelion 5', 'Yoshiyuki Sadamoto', 'Vuelve Neon Genesis Evangelion, uno de los mangas de culto más populares, pero esta vez lo hace en una fantástica edición coleccionista que los fans de la serie no podrán dejar escapar. Esta revolucionaria saga que marcó un antes y un después en su género mezcla ciencia ficción con un diseccionado análisis del alma humana que no deja indiferente a sus lectores...', 14.95, 25, 'neon_genesis_evangelion_col_5.png', 'Sci-Fi', 'Norma Editorial', datetime.now() - timedelta(weeks=2, hours=12), supplier_1.id_supplier)
    manga_12 = Manga('Neon Genesis Evangelion 6', 'Yoshiyuki Sadamoto', 'Vuelve Neon Genesis Evangelion, uno de los mangas de culto más populares, pero esta vez lo hace en una fantástica edición coleccionista que los fans de la serie no podrán dejar escapar. Esta revolucionaria saga que marcó un antes y un después en su género mezcla ciencia ficción con un diseccionado análisis del alma humana que no deja indiferente a sus lectores...', 14.95, 36, 'neon_genesis_evangelion_col_6.png', 'Sci-Fi', 'Norma Editorial', datetime.now() - timedelta(weeks=2, hours=12), supplier_1.id_supplier)
    manga_13 = Manga('Neon Genesis Evangelion 7', 'Yoshiyuki Sadamoto', 'Vuelve Neon Genesis Evangelion, uno de los mangas de culto más populares, pero esta vez lo hace en una fantástica edición coleccionista que los fans de la serie no podrán dejar escapar. Esta revolucionaria saga que marcó un antes y un después en su género mezcla ciencia ficción con un diseccionado análisis del alma humana que no deja indiferente a sus lectores...', 14.95, 123, 'neon_genesis_evangelion_col_7.png', 'Sci-Fi', 'Norma Editorial', datetime.now() - timedelta(weeks=2, hours=12), supplier_1.id_supplier)
    manga_14 = Manga('Ataque a los titanes Integral 1', 'Hajime Isayama', 'En un mundo dominado por el miedo a los titanes, la raza humana, convertida en mero alimento para esos seres, se protege de la invasión confinándose tras altísimos muros y aislándose del mundo exterior. Sin embargo, esa paz aparente se rompe con la aparición de un titán que, tras destruir el muro, inicia una nueva contienda que decidirá, de una vez por todas, quién se hará con la hegemonía en el mundo.', 24.50, 50, 'ataque_titanes_integral_1.png', 'Aventuras', 'Norma Editorial', datetime.now() - timedelta(weeks=2, hours=12), supplier_1.id_supplier)
    manga_15 = Manga('Hirayasumi 1', 'Keigo Shinzo', 'Hiroto Ikuta, 29 años, sin empleo fijo. Simplemente por su carácter bonachón, se hace amigo de una anciana del vecindario que le deja en herencia su casa unifamiliar. Así, empieza a vivir en ella junto a su prima Natsumi, de 18 años, que acaba de mudarse a la gran metrópolis tokiota. Es el inicio de una vida en una casita que, sin duda, ayudará a reparar las ansiedades, dudas y dificultades del día a día.', 9, 6, 'hirayasumi_1.png', 'Slice of Life', 'Milky Way Ediciones', datetime.now() - timedelta(weeks=2, hours=12), supplier_3.id_supplier)
    manga_16 = Manga('Hirayasumi 2', 'Keigo Shinzo', 'Hiroto Ikuta, 29 años, sin empleo fijo. Simplemente por su carácter bonachón, se hace amigo de una anciana del vecindario que le deja en herencia su casa unifamiliar. Así, empieza a vivir en ella junto a su prima Natsumi, de 18 años, que acaba de mudarse a la gran metrópolis tokiota. Es el inicio de una vida en una casita que, sin duda, ayudará a reparar las ansiedades, dudas y dificultades del día a día.', 9, 8, 'hirayasumi_2.png', 'Slice of Life', 'Milky Way Ediciones', datetime.now() - timedelta(weeks=2, hours=12), supplier_3.id_supplier)
    manga_17 = Manga('Hirayasumi 3', 'Keigo Shinzo', 'Hiroto Ikuta, 29 años, sin empleo fijo. Simplemente por su carácter bonachón, se hace amigo de una anciana del vecindario que le deja en herencia su casa unifamiliar. Así, empieza a vivir en ella junto a su prima Natsumi, de 18 años, que acaba de mudarse a la gran metrópolis tokiota. Es el inicio de una vida en una casita que, sin duda, ayudará a reparar las ansiedades, dudas y dificultades del día a día.', 9, 12, 'hirayasumi_3.png', 'Slice of Life', 'Milky Way Ediciones', datetime.now() - timedelta(weeks=2, hours=12), supplier_3.id_supplier)
    manga_18 = Manga('Hirayasumi 4', 'Keigo Shinzo', 'Hiroto Ikuta, 29 años, sin empleo fijo. Simplemente por su carácter bonachón, se hace amigo de una anciana del vecindario que le deja en herencia su casa unifamiliar. Así, empieza a vivir en ella junto a su prima Natsumi, de 18 años, que acaba de mudarse a la gran metrópolis tokiota. Es el inicio de una vida en una casita que, sin duda, ayudará a reparar las ansiedades, dudas y dificultades del día a día.', 9, 35, 'hirayasumi_4.png', 'Slice of Life', 'Milky Way Ediciones', datetime.now() - timedelta(weeks=2, hours=12), supplier_3.id_supplier)
    manga_19 = Manga('Hirayasumi 5', 'Keigo Shinzo', 'Hiroto Ikuta, 29 años, sin empleo fijo. Simplemente por su carácter bonachón, se hace amigo de una anciana del vecindario que le deja en herencia su casa unifamiliar. Así, empieza a vivir en ella junto a su prima Natsumi, de 18 años, que acaba de mudarse a la gran metrópolis tokiota. Es el inicio de una vida en una casita que, sin duda, ayudará a reparar las ansiedades, dudas y dificultades del día a día.', 9, 43, 'hirayasumi_5.png', 'Slice of Life', 'Milky Way Ediciones', datetime.now() - timedelta(weeks=2, hours=12), supplier_3.id_supplier)

    supplier_1.mangas_supplier.extend([manga_1, manga_10, manga_11, manga_12, manga_13, manga_14])
    supplier_2.mangas_supplier.extend([manga_2, manga_3, manga_4, manga_5, manga_6, manga_7, manga_8, manga_9])
    supplier_3.mangas_supplier.extend([manga_15, manga_16, manga_17, manga_18, manga_19])

    wishlist_1 = Wishlist(user_1.id_user, manga_8.id_manga)
    wishlist_2 = Wishlist(user_1.id_user, manga_13.id_manga)
    wishlist_3 = Wishlist(user_1.id_user, manga_16.id_manga)
    wishlist_4 = Wishlist(user_2.id_user, manga_13.id_manga)
    wishlist_5 = Wishlist(user_2.id_user, manga_17.id_manga)
    wishlist_6 = Wishlist(user_2.id_user, manga_9.id_manga)
    wishlist_7 = Wishlist(user_3.id_user, manga_12.id_manga)
    wishlist_8 = Wishlist(user_3.id_user, manga_19.id_manga)
    wishlist_9 = Wishlist(user_4.id_user, manga_13.id_manga)
    wishlist_10 = Wishlist(user_4.id_user, manga_18.id_manga)
    wishlist_11 = Wishlist(user_5.id_user, manga_7.id_manga)

    user_1.wishlists_user.extend([wishlist_1, wishlist_2, wishlist_3])
    user_2.wishlists_user.extend([wishlist_4, wishlist_5, wishlist_6])
    user_3.wishlists_user.extend([wishlist_7, wishlist_8])
    user_4.wishlists_user.extend([wishlist_9, wishlist_10])
    user_5.wishlists_user.extend([wishlist_11])
    manga_7.wishlists_manga.append(wishlist_11)
    manga_8.wishlists_manga.append(wishlist_1)
    manga_9.wishlists_manga.append(wishlist_6)
    manga_12.wishlists_manga.append(wishlist_7)
    manga_13.wishlists_manga.extend([wishlist_2, wishlist_4, wishlist_9])
    manga_16.wishlists_manga.append(wishlist_3)
    manga_17.wishlists_manga.append(wishlist_5)
    manga_18.wishlists_manga.append(wishlist_10)
    manga_19.wishlists_manga.append(wishlist_8)

    review_1 = Review(user_1.id_user, manga_19.id_manga, '¡Muy bueno!', 5, datetime.now() - timedelta(weeks=2, hours=12))
    review_2 = Review(user_1.id_user, manga_14.id_manga, 'Me encanta este manga.', 4, datetime.now() - timedelta(weeks=2, hours=12))
    review_3 = Review(user_1.id_user, manga_13.id_manga, 'La historia se desarrolla de forma excepcional.', 5, datetime.now() - timedelta(weeks=2, hours=12))
    review_4 = Review(user_2.id_user, manga_14.id_manga, 'No me ha convencido mucho.', 3, datetime.now() - timedelta(weeks=2, hours=12))
    review_5 = Review(user_2.id_user, manga_19.id_manga, '¡Increíble!', 4, datetime.now() - timedelta(weeks=2, hours=12))
    review_6 = Review(user_3.id_user, manga_13.id_manga, 'Está entretenido.', 4, datetime.now() - timedelta(weeks=2, hours=12))
    review_7 = Review(user_4.id_user, manga_9.id_manga, 'De lo mejor que he leído.', 5, datetime.now() - timedelta(weeks=2, hours=12))

    user_1.reviews_user.extend([review_1, review_2, review_3])
    user_2.reviews_user.extend([review_4, review_5])
    user_3.reviews_user.append(review_6)
    user_4.reviews_user.append(review_7)
    manga_9.reviews_manga.append(review_7)
    manga_13.reviews_manga.extend([review_3, review_6])
    manga_14.reviews_manga.extend([review_2, review_4])
    manga_19.reviews_manga.extend([review_1, review_5])

    payment_1 = Payment(datetime.now() - timedelta(weeks=2, hours=12), 'credit_card', 20.99, user_1.id_user)
    payment_2 = Payment(datetime.now() - timedelta(weeks=2, hours=12), 'credit_card', 52.99, user_1.id_user)
    payment_3 = Payment(datetime.now() - timedelta(weeks=2, hours=12), 'credit_card', 36.44, user_2.id_user)
    payment_4 = Payment(datetime.now() - timedelta(weeks=2, hours=12), 'credit_card', 48.84, user_2.id_user)
    payment_5 = Payment(datetime.now() - timedelta(weeks=2, hours=12), 'credit_card', 21.49, user_3.id_user)
    payment_6 = Payment(datetime.now() - timedelta(weeks=2, hours=12), 'credit_card', 12.49, user_3.id_user)
    payment_7 = Payment(datetime.now() - timedelta(weeks=2, hours=12), 'credit_card', 28.49, user_3.id_user)
    payment_8 = Payment(datetime.now() - timedelta(weeks=2, hours=12), 'credit_card', 12.99, user_1.id_user)
    payment_9 = Payment(datetime.now() - timedelta(weeks=2, hours=12), 'credit_card', 12.49, user_1.id_user)
    payment_10 = Payment(datetime.now() - timedelta(weeks=2, hours=12), 'credit_card', 61.99, user_1.id_user)
    payment_11 = Payment(datetime.now() - timedelta(weeks=2, hours=12), 'credit_card', 46.49, user_1.id_user)
    payment_12 = Payment(datetime.now() - timedelta(weeks=2, hours=12), 'credit_card', 28.49, user_1.id_user)
    payment_13 = Payment(datetime.now() - timedelta(weeks=2, hours=12), 'credit_card', 20.99, user_4.id_user)
    payment_14 = Payment(datetime.now() - timedelta(weeks=2, hours=12), 'credit_card', 36.49, user_4.id_user)
    payment_15 = Payment(datetime.now() - timedelta(weeks=2, hours=12), 'credit_card', 36.99, user_4.id_user)
    payment_16 = Payment(datetime.now() - timedelta(weeks=2, hours=12), 'credit_card', 21.49, user_6.id_user)
    payment_17 = Payment(datetime.now() - timedelta(weeks=2, hours=12), 'credit_card', 29.49, user_6.id_user)
    payment_18 = Payment(datetime.now() - timedelta(weeks=2, hours=12), 'credit_card', 30.99, user_8.id_user)
    payment_19 = Payment(datetime.now() - timedelta(weeks=2, hours=12), 'credit_card', 28.49, user_8.id_user)
    payment_20 = Payment(datetime.now() - timedelta(weeks=2, hours=12), 'credit_card', 12.49, user_8.id_user)
    payment_21 = Payment(datetime.now() - timedelta(weeks=2, hours=12), 'credit_card', 37.49, user_8.id_user)
    payment_22 = Payment(datetime.now() - timedelta(weeks=2, hours=12), 'credit_card', 28.49, user_11.id_user)
    payment_23 = Payment(datetime.now() - timedelta(weeks=2, hours=12), 'credit_card', 21.99, user_11.id_user)

    user_1.payments_user.extend([payment_1, payment_2, payment_8, payment_9, payment_10, payment_11, payment_12])
    user_2.payments_user.extend([payment_3, payment_4])
    user_3.payments_user.extend([payment_5, payment_6, payment_7])
    user_4.payments_user.extend([payment_13, payment_14, payment_15])
    user_6.payments_user.extend([payment_16, payment_17])
    user_8.payments_user.extend([payment_18, payment_19, payment_20, payment_21])
    user_11.payments_user.extend([payment_22, payment_23])

    order_1 = Order(datetime.now() - timedelta(weeks=2, hours=12), 'pending', 20.99, payment_1.id_payment, address_1.id_address)
    order_2 = Order(datetime.now() - timedelta(weeks=2, hours=12), 'pending', 52.99, payment_2.id_payment, address_1.id_address)
    order_3 = Order(datetime.now() - timedelta(weeks=2, hours=12), 'pending', 36.44, payment_3.id_payment, address_2.id_address)
    order_4 = Order(datetime.now() - timedelta(weeks=2, hours=12), 'sent', 48.84, payment_4.id_payment, address_2.id_address)
    order_5 = Order(datetime.now() - timedelta(weeks=2, hours=12), 'sent', 21.49, payment_5.id_payment, address_3.id_address)
    order_6 = Order(datetime.now() - timedelta(weeks=2, hours=12), 'sent', 12.49, payment_6.id_payment, address_3.id_address)
    order_7 = Order(datetime.now() - timedelta(weeks=2, hours=12), 'sent', 28.49, payment_7.id_payment, address_3.id_address)
    order_8 = Order(datetime.now() - timedelta(weeks=2, hours=12), 'sent', 12.99, payment_8.id_payment, address_1.id_address)
    order_9 = Order(datetime.now() - timedelta(weeks=2, hours=12), 'sent', 12.49, payment_9.id_payment, address_1.id_address)
    order_10 = Order(datetime.now() - timedelta(weeks=2, hours=12), 'sent', 61.99, payment_10.id_payment, address_1.id_address)
    order_11 = Order(datetime.now() - timedelta(weeks=2, hours=12), 'sent', 46.49, payment_11.id_payment, address_1.id_address)
    order_12 = Order(datetime.now() - timedelta(weeks=2, hours=12), 'sent', 28.49, payment_12.id_payment, address_1.id_address)
    order_13 = Order(datetime.now() - timedelta(weeks=2, hours=12), 'sent', 20.99, payment_13.id_payment, address_4.id_address)
    order_14 = Order(datetime.now() - timedelta(weeks=2, hours=12), 'sent', 36.49, payment_14.id_payment, address_4.id_address)
    order_15 = Order(datetime.now() - timedelta(weeks=2, hours=12), 'sent', 36.99, payment_15.id_payment, address_4.id_address)
    order_16 = Order(datetime.now() - timedelta(weeks=2, hours=12), 'sent', 21.49, payment_16.id_payment, address_6.id_address)
    order_17 = Order(datetime.now() - timedelta(weeks=2, hours=12), 'sent', 29.49, payment_17.id_payment, address_6.id_address)
    order_18 = Order(datetime.now() - timedelta(weeks=2, hours=12), 'sent', 30.99, payment_18.id_payment, address_8.id_address)
    order_19 = Order(datetime.now() - timedelta(weeks=2, hours=12), 'sent', 28.49, payment_19.id_payment, address_8.id_address)
    order_20 = Order(datetime.now() - timedelta(weeks=2, hours=12), 'sent', 12.49, payment_20.id_payment, address_8.id_address)
    order_21 = Order(datetime.now() - timedelta(weeks=2, hours=12), 'sent', 37.49, payment_21.id_payment, address_8.id_address)
    order_22 = Order(datetime.now() - timedelta(weeks=2, hours=12), 'sent', 28.49, payment_22.id_payment, address_11.id_address)
    order_23 = Order(datetime.now() - timedelta(weeks=2, hours=12), 'sent', 21.99, payment_23.id_payment, address_11.id_address)

    payment_1.order_payments.append(order_1)
    payment_2.order_payments.append(order_2)
    payment_3.order_payments.append(order_3)
    payment_4.order_payments.append(order_4)
    payment_5.order_payments.append(order_5)
    payment_6.order_payments.append(order_6)
    payment_7.order_payments.append(order_7)
    payment_8.order_payments.append(order_8)
    payment_9.order_payments.append(order_9)
    payment_10.order_payments.append(order_10)
    payment_11.order_payments.append(order_11)
    payment_12.order_payments.append(order_12)
    payment_13.order_payments.append(order_13)
    payment_14.order_payments.append(order_14)
    payment_15.order_payments.append(order_15)
    payment_16.order_payments.append(order_16)
    payment_17.order_payments.append(order_17)
    payment_18.order_payments.append(order_18)
    payment_19.order_payments.append(order_19)
    payment_20.order_payments.append(order_20)
    payment_21.order_payments.append(order_21)
    payment_22.order_payments.append(order_22)
    payment_23.order_payments.append(order_23)
    address_1.orders_address.extend([order_1, order_2, order_8, order_9, order_10, order_11, order_12])
    address_2.orders_address.extend([order_3, order_4])
    address_3.orders_address.extend([order_5, order_6, order_7])
    address_4.orders_address.extend([order_13, order_14, order_15])
    address_6.orders_address.extend([order_16, order_17])
    address_8.orders_address.extend([order_18, order_19, order_20, order_21])
    address_11.orders_address.extend([order_22, order_23])

    order_manga_1 = OrderManga(order_1.id_order, manga_7.id_manga, 1)
    order_manga_2 = OrderManga(order_1.id_order, manga_9.id_manga, 1)
    order_manga_3 = OrderManga(order_2.id_order, manga_14.id_manga, 2)
    order_manga_4 = OrderManga(order_3.id_order, manga_13.id_manga, 1)
    order_manga_5 = OrderManga(order_3.id_order, manga_5.id_manga, 1)
    order_manga_6 = OrderManga(order_3.id_order, manga_16.id_manga, 2)
    order_manga_7 = OrderManga(order_4.id_order, manga_12.id_manga, 3)
    order_manga_8 = OrderManga(order_5.id_order, manga_1.id_manga, 1)
    order_manga_9 = OrderManga(order_5.id_order, manga_5.id_manga, 2)
    order_manga_10 = OrderManga(order_6.id_order, manga_3.id_manga, 2)
    order_manga_11 = OrderManga(order_7.id_order, manga_14.id_manga, 1)
    order_manga_12 = OrderManga(order_8.id_order, manga_19.id_manga, 1)
    order_manga_13 = OrderManga(order_9.id_order, manga_6.id_manga, 1)
    order_manga_14 = OrderManga(order_10.id_order, manga_11.id_manga, 4)
    order_manga_15 = OrderManga(order_11.id_order, manga_9.id_manga, 5)
    order_manga_16 = OrderManga(order_12.id_order, manga_14.id_manga, 1)
    order_manga_17 = OrderManga(order_13.id_order, manga_8.id_manga, 1)
    order_manga_18 = OrderManga(order_13.id_order, manga_9.id_manga, 1)
    order_manga_19 = OrderManga(order_14.id_order, manga_11.id_manga, 1)
    order_manga_20 = OrderManga(order_14.id_order, manga_18.id_manga, 1)
    order_manga_21 = OrderManga(order_14.id_order, manga_1.id_manga, 1)
    order_manga_22 = OrderManga(order_15.id_order, manga_14.id_manga, 1)
    order_manga_23 = OrderManga(order_15.id_order, manga_17.id_manga, 1)
    order_manga_24 = OrderManga(order_16.id_order, manga_1.id_manga, 1)
    order_manga_25 = OrderManga(order_16.id_order, manga_6.id_manga, 1)
    order_manga_26 = OrderManga(order_17.id_order, manga_8.id_manga, 1)
    order_manga_27 = OrderManga(order_17.id_order, manga_7.id_manga, 1)
    order_manga_28 = OrderManga(order_17.id_order, manga_6.id_manga, 1)
    order_manga_29 = OrderManga(order_18.id_order, manga_1.id_manga, 3)
    order_manga_30 = OrderManga(order_19.id_order, manga_12.id_manga, 1)
    order_manga_31 = OrderManga(order_20.id_order, manga_4.id_manga, 1)
    order_manga_32 = OrderManga(order_21.id_order, manga_14.id_manga, 1)
    order_manga_33 = OrderManga(order_21.id_order, manga_1.id_manga, 1)
    order_manga_34 = OrderManga(order_22.id_order, manga_14.id_manga, 1)
    order_manga_35 = OrderManga(order_23.id_order, manga_15.id_manga, 2)

    order_1.orders_mangas_order.extend([order_manga_1, order_manga_2])
    order_2.orders_mangas_order.append(order_manga_3)
    order_3.orders_mangas_order.extend([order_manga_4, order_manga_5, order_manga_6])
    order_4.orders_mangas_order.append(order_manga_7)
    order_5.orders_mangas_order.extend([order_manga_8, order_manga_9])
    order_6.orders_mangas_order.append(order_manga_10)
    order_7.orders_mangas_order.append(order_manga_11)
    order_8.orders_mangas_order.append(order_manga_12)
    order_9.orders_mangas_order.append(order_manga_13)
    order_10.orders_mangas_order.append(order_manga_14)
    order_11.orders_mangas_order.append(order_manga_15)
    order_12.orders_mangas_order.append(order_manga_16)
    order_13.orders_mangas_order.extend([order_manga_17, order_manga_18])
    order_14.orders_mangas_order.extend([order_manga_19, order_manga_20, order_manga_21])
    order_15.orders_mangas_order.extend([order_manga_22, order_manga_23])
    order_16.orders_mangas_order.extend([order_manga_24, order_manga_25])
    order_17.orders_mangas_order.extend([order_manga_26, order_manga_27, order_manga_28])
    order_18.orders_mangas_order.append(order_manga_29)
    order_19.orders_mangas_order.append(order_manga_30)
    order_20.orders_mangas_order.append(order_manga_31)
    order_21.orders_mangas_order.extend([order_manga_32, order_manga_33])
    order_22.orders_mangas_order.append(order_manga_34)
    order_23.orders_mangas_order.append(order_manga_35)
    manga_1.orders_mangas_manga.extend([order_manga_8, order_manga_21, order_manga_24, order_manga_29, order_manga_33])
    manga_3.orders_mangas_manga.append(order_manga_10)
    manga_4.orders_mangas_manga.append(order_manga_31)
    manga_5.orders_mangas_manga.extend([order_manga_5, order_manga_9])
    manga_6.orders_mangas_manga.extend([order_manga_13, order_manga_25, order_manga_28])
    manga_7.orders_mangas_manga.extend([order_manga_1, order_manga_27])
    manga_8.orders_mangas_manga.extend([order_manga_17, order_manga_26])
    manga_9.orders_mangas_manga.extend([order_manga_2, order_manga_15, order_manga_18])
    manga_11.orders_mangas_manga.extend([order_manga_14, order_manga_19])
    manga_12.orders_mangas_manga.extend([order_manga_7, order_manga_30])
    manga_13.orders_mangas_manga.append(order_manga_4)
    manga_14.orders_mangas_manga.extend([
        order_manga_3, order_manga_11, order_manga_16, order_manga_22, order_manga_32, order_manga_34
    ])
    manga_15.orders_mangas_manga.append(order_manga_35)
    manga_16.orders_mangas_manga.append(order_manga_6)
    manga_17.orders_mangas_manga.append(order_manga_23)
    manga_18.orders_mangas_manga.append(order_manga_20)
    manga_19.orders_mangas_manga.append(order_manga_12)

    new_1 = New('Blue Period entra en pausa hasta primavera de 2024', 'El número de enero de la revista Monthly Afternoon reveló el sábado que el manga Blue Period volverá a entrar en pausa por un tiempo. La obra de Yamaguchi Tsubasa regresará a las páginas de la revista mensual de Kodansha en algún momento de la próxima primavera de 2024.\n Tsubasa Yamaguchi, autora de este premiado manga, comenzó su publicación en junio de 2017 en las páginas de la revista Monthly Afternoon de Kodansha y cuenta a día de hoy con 15 tomos recopilatorios en el mercado japonés. La obra fue premiada en la edición 13 de los premios Manga Taisho Awards y en los Kodansha Manga Award, en la categoría general, en 2020. La historia de Yatora Yaguchi inspiró una serie de animación de 12 episodios animados por Seven Arcs y dirigidos por Koji Masunari y Katsuya Asano, siendo emitidos estos entre octubre y diciembre de 2021.\n El manga de Blue Period está siendo publicado en España por Milky Way Ediciones. La editorial asturiana comenzó su publicación en octubre de 2019 y lanzó el decimotercer tomo en mayo de este 2023. La serie animada está disponible actualmente en Netflix.', 'manga', datetime.now() - timedelta(weeks=2, hours=12), user_1.id_user)  # 27 / 11 / 2023
    new_2 = New('Confirmado el anime de Nina del reino de las estrellas', 'La portada del número de enero de 2024 de la revista Be Love, que saldrá a la venta en Japón el 1 de diciembre, anuncia la adaptación al anime del manga Nina del reino de las estrellas (Hoshifuru Ōkoku no Nina). El magazine mensual confirma así los rumores sobre una posible adaptación del manga de Rikachi.\n Hoshifuru Ōkoku no Nina, título original en japonés, es un manga josei de fantasía y romance escrito y dibujado por Rikachi que se serializa desde octubre de 2019 en las páginas de la revista Be Love de Kodansha. La obra permanece abierta a día de hoy con 11 tomos recopilatorios en el mercado japonés y fue galardonada con el premio a mejor shôjo en la edición 46 de los premios Kodansha Manga Award en 2022.\n El manga está siendo editado en castellano por Arechi Manga, la cual comenzó su publicación en diciembre de 2022 en una edición en rústica de tapa blanda y con sobrecubierta 128×182 mm. y de la cual ya ha publicado los tres primeros tomos.', 'anime', datetime.now() - timedelta(weeks=2, hours=12), user_1.id_user)  # 28 / 11 / 2023
    new_3 = New('Un hombre ha sido arrestado por subir el manga de Liar Game', 'La Asociación Japonesa de Derechos de Autor para el Software de Ordenador (ACCS) anunció el pasado miércoles que el día anterior, el martes 24 de marzo, la unidad anti-ciber crimen de la prefectura de Chiba arrestó en Shinagawa (Tokyo) a un hombre de 36 años y sin trabajo acusándolo de violar la ley de propiedad intelectual japonesa.\n Al parecer, el sujeto usó el programa para compartir ficheros llamado Share y subió a Internet, sin permiso ni del autor ni de la editorial, el capítulo 197 del manga Liar Game. Este es dibujado por Shinonbu Kaitani y publicado en Japón por Shueisha. El capítulo compartido ilegalmente fue descargado por una gran cantidad de usuarios. Según la policía, el sujeto también había subido a la red muchos otros mangas y animes sin permiso de sus autores.\n La ley de propiedad intelectual japonesa no solo prohibe subir contenido a internet sin la autorización de los propietarios de su copyright, sino que fue modificada en 2009 por el parlamento japonés para criminalizar la descarga ilegal de contenido con copyright. Desde entonces, no pocas personas han sido arrestadas en Japón por subir a Internet anime, manga y juegos sin permiso de sus creadores. Muchos de los cuales subieron las obras a Internet a través de aplicaciones para compartir ficheros como Share o Perfect Dark. Sin embargo, el número de arrestos en Japón por descargas ilegales de contenido con copyright es bastante más excepcional. Por no decir que a fecha de hoy no existe ningún precedente.', 'japan', datetime.now() - timedelta(weeks=2, hours=12), user_1.id_user)  # 26 / 11 / 2023

    user_1.news_user.extend([new_1, new_2, new_3])

    users = [user_1, user_2, user_3, user_4, user_5, user_6, user_7, user_8, user_9, user_10, user_11, user_12]
    addresses = [
        address_1, address_2, address_3, address_4, address_5, address_6, address_7, address_8, address_9, address_10,
        address_11, address_12
    ]
    suppliers = [supplier_1, supplier_2, supplier_3]
    mangas = [
        manga_1, manga_2, manga_3, manga_4, manga_5, manga_6, manga_7, manga_8, manga_9, manga_10, manga_11, manga_12,
        manga_13, manga_14, manga_15, manga_16, manga_17, manga_18, manga_19
    ]
    wishlists = [
        wishlist_1, wishlist_2, wishlist_3, wishlist_4, wishlist_5, wishlist_6, wishlist_7, wishlist_8, wishlist_9,
        wishlist_10, wishlist_11
    ]
    reviews = [review_1, review_2, review_3, review_4, review_5, review_6, review_7]
    payments = [
        payment_1, payment_2, payment_3, payment_4, payment_5, payment_6, payment_7, payment_8, payment_9, payment_10,
        payment_11, payment_12, payment_13, payment_14, payment_15, payment_16, payment_17, payment_18, payment_19,
        payment_20, payment_21, payment_22, payment_23
    ]
    orders = [
        order_1, order_2, order_3, order_4, order_5, order_6, order_7, order_8, order_9, order_10, order_11, order_12,
        order_13, order_14, order_15, order_16, order_17, order_18, order_19, order_20, order_21, order_22, order_23
    ]
    orders_mangas = [
        order_manga_1, order_manga_2, order_manga_3, order_manga_4, order_manga_5, order_manga_6, order_manga_7,
        order_manga_8, order_manga_9, order_manga_10, order_manga_11, order_manga_12, order_manga_13, order_manga_14,
        order_manga_15, order_manga_16, order_manga_17, order_manga_18, order_manga_19, order_manga_20, order_manga_21,
        order_manga_22, order_manga_23, order_manga_24, order_manga_25, order_manga_26, order_manga_27, order_manga_28,
        order_manga_29, order_manga_30, order_manga_31, order_manga_32, order_manga_33, order_manga_34, order_manga_35
    ]
    news = [new_1, new_2, new_3]

    data = [users + addresses + suppliers + mangas + wishlists + reviews + payments + orders + orders_mangas + news]

    return data
