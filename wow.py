import discord

from random import seed
from random import randint

def wow(received):
    seed()
    selector = randint(1, 5)

    if selector == 1:
        embed = discord.Embed(
                              color=discord.Colour.random(),
                              title='✧･ﾟ: *✧･☆Wow!☆･ﾟ✧*:･ﾟ✧',
                              url='https://youtu.be/BnTdfA5aTpY',
                              description=':sparkles:Woooooooooow!:sparkles:'
                             )
        embed.set_author(
                         name="Childlike Wonder", 
                         url="https://twitter.com/vgdunkey",
                         icon_url="https://cdna.artstation.com/p/assets/images/images/019/293/032/large/kiki-andriansyah-hex-y.jpg?1562838735"
                        )
        embed.set_thumbnail(
                            url="https://thumbs.dreamstime.com/b/cute-rainbow-star-vector-illustration-design-142652749.jpg"
                           )
    if selector == 2:
        embed = discord.Embed(
                              color=discord.Colour.random(),
                              title='Wow.',
                              url='https://youtu.be/mBr8mcLj9QY',
                              description='Waow.'
                             )
        embed.set_author(
                         name="wOwen Wilson", 
                         url="https://twitter.com/owenwilson1",
                         icon_url="https://pbs.twimg.com/profile_images/576225660424835073/xnZxzQVE_400x400.jpeg"
                        )
        embed.set_thumbnail(
                            url="https://media.vanityfair.com/photos/5e348a5a26aeb300090a8423/5:3/w_2000,h_1200,c_limit/owen-wilson-loki.jpg"
                           )

    if selector == 3:
        embed = discord.Embed(
                              color=discord.Colour.random(),
                              title='waow. waow. waow.',
                              url='https://youtu.be/NhYz-Zij630',
                              description="Hey I'm Owen Wilson look at my nose waow"
                             )
        embed.set_author(
                         name="Owen Noseson", 
                         url="https://twitter.com/berdyaboi",
                         icon_url="https://i.ytimg.com/vi/LtNvVYFn79Q/mqdefault.jpg"
                        )
        embed.set_thumbnail(
                            url="https://i.ytimg.com/vi/LtNvVYFn79Q/mqdefault.jpg"
                           )

    if selector == 4:
        embed = discord.Embed(
                              color=discord.Colour.random(),
                              title='wohw.',
                              url='https://youtu.be/TRIwAHX3aHM',
                              description="wowh."
                             )
        embed.set_author(
                         name="nOwen Wilson", 
                         url="https://en.wikipedia.org/wiki/Owen_Wilson",
                         icon_url="https://en.wikipedia.org/wiki/Owen_Wilson#/media/File:Owen_Wilson_Cannes_2011.jpg"
                        )
        embed.set_thumbnail(
                url="https://thumbs.dreamstime.com/b/vector-illusration-lettering-wow-word-lettering-wow-word-vector-illusration-168640093.jpg"

    if selector == 5:
        embed = discord.Embed(
                              color=discord.Colour.random(),
                              title='Waowh.',
                              url='https://youtu.be/-0WSkGVlt7Q',
                              description="waowh."
                             )
        embed.set_author(
                         name="Wow Guy", 
                         url="https://en.wikipedia.org/wiki/Eddy_Wally",
                         icon_url="https://en.wikipedia.org/wiki/Eddy_Wally#/media/File:EddyWallyBertHeymans.jpg"
                        )
        embed.set_thumbnail(
                         url="https://i.ytimg.com/vi/Xm_dS-wEFvs/maxresdefault.jpg"
                           )

    return embed
