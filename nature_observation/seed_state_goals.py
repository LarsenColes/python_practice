import sqlite3
from main import NatureObservationTool

def seed_state_goals():
    """Seed the database with sample goals for different US states."""
    tool = NatureObservationTool()
    
    # Clear existing goals - establish a direct connection
    conn = sqlite3.connect(tool.db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM goals')
    conn.commit()
    conn.close()
    
    # New York State Goals
    tool.add_goal("Find a sugar maple leaf and identify its distinctive shape", "NY", 1, "plants", "fall")
    tool.add_goal("Spot an eastern gray squirrel gathering food", "NY", 1, "mammals")
    tool.add_goal("Identify a black-capped chickadee by its call", "NY", 1, "birds")
    tool.add_goal("Find a white-tailed deer or its tracks", "NY", 2, "mammals")
    tool.add_goal("Locate a red oak tree and collect an acorn", "NY", 1, "plants", "fall")
    tool.add_goal("Spot a blue jay with its bright blue feathers", "NY", 1, "birds")
    tool.add_goal("Find a garter snake basking in the sun", "NY", 2, "reptiles", "summer")
    tool.add_goal("Identify a red-tailed hawk soaring overhead", "NY", 2, "birds")
    tool.add_goal("Locate a patch of trillium flowers in a forest", "NY", 2, "plants", "spring")
    tool.add_goal("Find a painted turtle on a log", "NY", 2, "reptiles", "summer")
    tool.add_goal("Identify a northern cardinal by its bright red color", "NY", 1, "birds")
    tool.add_goal("Find a patch of fiddlehead ferns in the spring", "NY", 2, "plants", "spring")
    tool.add_goal("Spot a monarch butterfly on milkweed", "NY", 2, "insects", "summer")
    tool.add_goal("Look for woodpecker holes in tree trunks", "NY", 1, "birds")
    tool.add_goal("Find a salamander under a log (replace the log carefully!)", "NY", 3, "amphibians")
    
    # Additional plant goals for New York
    tool.add_goal("Find a white pine tree and count the needles in a bundle (should be 5)", "NY", 1, "plants")
    tool.add_goal("Identify a striped maple tree by its distinctive bark", "NY", 2, "plants")
    tool.add_goal("Find a witch hazel plant and check for its unique flowers or seed pods", "NY", 2, "plants")
    tool.add_goal("Locate a Jack-in-the-pulpit in a woodland area", "NY", 2, "plants", "spring")
    tool.add_goal("Find a patch of wild strawberries", "NY", 1, "plants", "summer")
    tool.add_goal("Identify a hemlock tree by its small cones and flat needles", "NY", 2, "plants")
    tool.add_goal("Locate a mayapple plant with its umbrella-like leaf", "NY", 1, "plants", "spring")
    tool.add_goal("Find a black cherry tree and identify it by its bark (looks like burnt potato chips)", "NY", 2, "plants")
    tool.add_goal("Identify a beech tree by its smooth gray bark", "NY", 1, "plants")
    tool.add_goal("Find three different species of fern", "NY", 2, "plants", "summer")
    tool.add_goal("Locate a skunk cabbage in a wetland area", "NY", 1, "plants", "spring")
    tool.add_goal("Find goldenrod in bloom", "NY", 1, "plants", "fall")
    tool.add_goal("Identify a white oak tree by its rounded leaf lobes", "NY", 2, "plants")
    tool.add_goal("Find a patch of wild blueberries or huckleberries", "NY", 2, "plants", "summer")
    tool.add_goal("Locate a yellow birch tree and smell its wintergreen-scented bark", "NY", 2, "plants")
    tool.add_goal("Find a clump of cattails in a wetland", "NY", 1, "plants")
    tool.add_goal("Identify a maple tree by its samara (helicopter seeds)", "NY", 1, "plants", "fall")
    tool.add_goal("Find three different kinds of mosses on rocks or trees", "NY", 2, "plants")
    tool.add_goal("Locate a wild apple tree", "NY", 1, "plants")
    tool.add_goal("Find wild grape vines climbing a tree", "NY", 1, "plants")
    tool.add_goal("Identify an ash tree by its compound leaves", "NY", 2, "plants")
    tool.add_goal("Find a patch of wood sorrel (looks like clover with heart-shaped leaves)", "NY", 1, "plants")
    tool.add_goal("Locate a sassafras tree with its mitten-shaped leaves", "NY", 2, "plants")
    tool.add_goal("Find a mountain laurel bush", "NY", 2, "plants")
    tool.add_goal("Identify jewelweed and gently touch a ripe seed pod to see it burst", "NY", 1, "plants", "summer")
    
    # California Goals
    tool.add_goal("Find a California poppy in bloom", "CA", 1, "plants", "spring")
    tool.add_goal("Identify a scrub jay by its blue and gray colors", "CA", 1, "birds")
    tool.add_goal("Spot a ground squirrel near its burrow", "CA", 1, "mammals")
    tool.add_goal("Find a redwood tree and appreciate its size", "CA", 1, "plants")
    tool.add_goal("Identify a hummingbird visiting flowers", "CA", 2, "birds")
    tool.add_goal("Find a manzanita bush with its distinctive red bark", "CA", 1, "plants")
    tool.add_goal("Spot a western fence lizard doing push-ups", "CA", 2, "reptiles", "summer")
    tool.add_goal("Locate a California live oak tree", "CA", 1, "plants")
    tool.add_goal("Find evidence of wild turkey activity", "CA", 2, "birds")
    tool.add_goal("Spot a California quail with its topknot", "CA", 2, "birds")
    tool.add_goal("Find a banana slug in a damp area", "CA", 1, "invertebrates")
    tool.add_goal("Identify poison oak (but don't touch!)", "CA", 1, "plants")
    tool.add_goal("Spot a black-tailed deer", "CA", 2, "mammals")
    tool.add_goal("Find a coastal tide pool and observe its inhabitants", "CA", 2, "marine", "summer")
    tool.add_goal("Identify a valley oak tree", "CA", 1, "plants")
    
    # Texas Goals
    tool.add_goal("Find a Texas bluebonnet flower (spring)", "TX", 1, "plants", "spring")
    tool.add_goal("Spot a roadrunner", "TX", 2, "birds")
    tool.add_goal("Identify a mockingbird (Texas state bird) by its varied calls", "TX", 1, "birds")
    tool.add_goal("Find a live oak tree with its spreading branches", "TX", 1, "plants")
    tool.add_goal("Spot an armadillo or its burrow", "TX", 2, "mammals")
    tool.add_goal("Find a prickly pear cactus", "TX", 1, "plants")
    tool.add_goal("Identify a scissor-tailed flycatcher by its long tail", "TX", 2, "birds", "summer")
    tool.add_goal("Find a horned lizard", "TX", 3, "reptiles", "summer")
    tool.add_goal("Locate a mesquite tree", "TX", 1, "plants")
    tool.add_goal("Spot a red-tailed hawk perched or soaring", "TX", 2, "birds")
    tool.add_goal("Find a Texas persimmon tree", "TX", 2, "plants")
    tool.add_goal("Identify wildflowers along a roadside", "TX", 1, "plants", "spring")
    tool.add_goal("Spot a coyote or its tracks", "TX", 3, "mammals")
    tool.add_goal("Find a monarch butterfly during migration season", "TX", 2, "insects", "fall")
    tool.add_goal("Locate a cypress tree near water", "TX", 1, "plants")
    
    # Florida Goals
    tool.add_goal("Spot an anhinga drying its wings", "FL", 2, "birds")
    tool.add_goal("Find a Spanish moss hanging from an oak tree", "FL", 1, "plants")
    tool.add_goal("Identify a palm tree (cabbage palm is Florida's state tree)", "FL", 1, "plants")
    tool.add_goal("Spot an alligator sunning itself", "FL", 2, "reptiles")
    tool.add_goal("Find a great blue heron fishing", "FL", 1, "birds")
    tool.add_goal("Identify a sea grape plant near the coast", "FL", 1, "plants")
    tool.add_goal("Find a gopher tortoise or its burrow", "FL", 2, "reptiles")
    tool.add_goal("Spot an osprey nest on a platform or pole", "FL", 2, "birds")
    tool.add_goal("Find a mangrove tree with its prop roots", "FL", 1, "plants")
    tool.add_goal("Identify an anole lizard changing colors", "FL", 1, "reptiles")
    tool.add_goal("Spot a roseate spoonbill with its pink coloration", "FL", 3, "birds")
    tool.add_goal("Find a cypress knee poking out of the water", "FL", 1, "plants")
    tool.add_goal("Identify a mockingbird singing", "FL", 1, "birds")
    tool.add_goal("Find saw palmetto plants", "FL", 1, "plants")
    tool.add_goal("Spot a wood stork", "FL", 2, "birds")
    
    # More states can be added similarly...
    
    # Generic goals (will work anywhere in the US)
    tool.add_goal("Find three different shaped leaves", "Unknown", 1, "plants")
    tool.add_goal("Identify a bird by its song", "Unknown", 2, "birds")
    tool.add_goal("Find evidence of animal activity (tracks, scat, etc.)", "Unknown", 1, "mammals")
    tool.add_goal("Spot a butterfly", "Unknown", 1, "invertebrates", "summer")
    tool.add_goal("Find a spider web with dew drops", "Unknown", 1, "invertebrates", "morning")
    tool.add_goal("Locate three different types of clouds in the sky", "Unknown", 1, "weather")
    tool.add_goal("Find a wildflower and photograph it", "Unknown", 1, "plants", "spring")
    tool.add_goal("Spot a squirrel gathering food", "Unknown", 1, "mammals")
    tool.add_goal("Find a naturally fallen leaf that's still intact", "Unknown", 1, "plants", "fall")
    tool.add_goal("Look for birds building nests", "Unknown", 2, "birds", "spring")
    tool.add_goal("Find a rock with an interesting pattern or shape", "Unknown", 1, "geology")
    tool.add_goal("Identify three different bird species", "Unknown", 2, "birds")
    tool.add_goal("Find an insect pollinating a flower", "Unknown", 1, "insects", "summer")
    tool.add_goal("Locate a mushroom or fungus growing on a log", "Unknown", 1, "fungi")
    tool.add_goal("Observe an ant colony at work", "Unknown", 1, "insects")
    
    print("State-specific goals database seeded successfully!")

if __name__ == "__main__":
    seed_state_goals() 