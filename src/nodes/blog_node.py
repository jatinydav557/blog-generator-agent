from src.states.blogstate import BlogState
from langchain_core.messages import SystemMessage, HumanMessage
from src.states.blogstate import Blog

class BlogNode:
    """
    A class to represent he blog node
    """

    def __init__(self,llm):
        self.llm=llm
   
    def title_creation(self,state:BlogState):
        """
        create the title for the blog
        """

        if "topic" in state and state["topic"]:
            prompt="""
                   You are an expert blog content writer. Use Markdown formatting. Generate
                   a blog title for the {topic}. This title should be creative and SEO friendly
                   and should be of one line.

                   """
            sytem_message=prompt.format(topic=state["topic"])
            print(sytem_message)
            response=self.llm.invoke(sytem_message)
            print(response)
            return {"blog":{"title":response.content}}
        
    def content_generation(self,state:BlogState):
        if "topic" in state and state["topic"]:
            system_prompt = """You are expert blog writer. Use Markdown formatting.
            Generate a detailed blog content with detailed breakdown for the {topic}"""
            system_message = system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": state['blog']['title'], "content": response.content}}
        
    def translation(self,state:BlogState):
        translation_prompt = f"""
        Translate the following content into {state["current_language"]}.
        - Maintain the original tone, style, and formatting.
        - Adapt cultural references and idioms to be appropriate for {state["current_language"]}.

        ORIGINAL CONTENT:
        {state["blog"]["content"]}
        """

        messages = [HumanMessage(translation_prompt)]
        response = self.llm.invoke(messages)
        
        return {"blog": {"title": state["blog"]["title"], "content": response.content}}


    def route(self, state: BlogState):
        return {"current_language": state['current_language'] }
    

    def route_decision(self, state: BlogState):
        """
        Route the content to the respective translation function.
        """
        if state["current_language"] == "hindi":
            return "hindi"
        elif state["current_language"] == "french": 
            return "french"
        else:
            return state['current_language']
