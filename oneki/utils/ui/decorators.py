import discord
from discord import ui 
from typing import Union
import functools


def component(deco):
    def decorator(func):
        @deco
        async def callback_wrapper(self, interaction: discord.Interaction, component: Union[ui.Button, ui.Select]):
            translation = self.translations[func.__name__]
            await func(self, interaction, component, translation)
        
        return callback_wrapper
    
    return decorator
        
    
def button(**kwargs):
    return component(ui.button(**kwargs))
    
    
def change_color_when_used(func): 
    @functools.wraps(func)
    async def callback_wrapper(self, interaction, button, translation):
        if getattr(self, "button_used", None) is not None:
            self.button_used.style = discord.ButtonStyle.secondary
                    
        button.style = discord.ButtonStyle.success
        self.button_used = button
        
        await func(self, interaction, button, translation)

    return callback_wrapper

def disable_when_pressed(func):
    @functools.wraps(func)
    async def callback_wrapper(self, interaction, component, translation):
        try:
            data = await func(self, interaction, component, translation)
        finally:
            await self.disable(**data)

    return callback_wrapper
    
    
def select(**kwargs):
    return component(ui.select(**kwargs))