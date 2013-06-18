from eos import Ship, Skill
from eos.fit import Fit

from const import Attribute, Skills

import math


class RFit(Fit):
  """Inherits from eos' Fit and adds high-level methods."""
  def __init__(self, typeID):
    super().__init__()
    self.ship = Ship(typeID)

    # Set all skills to level V.
    for skill in Skills.allSkills:
      self.skills.add(Skill(skill, level=5))

    self.validate()

  @property
  def scanResolution(self):
    """Returns the scan resolution in mm of the ship."""
    try:
      return self.ship.attributes[Attribute.scanResolution]
    except (AttributeError, KeyError):
      return None

  @property
  def targetRange(self):
    """Returns the max target range in km of the ship."""
    try:
      return self.ship.attributes[Attribute.targetRange] / 1000
    except (AttributeError, KeyError):
      return None

  @property
  def maxTargets(self):
    """Returns the max number of locked targets."""
    try:
      return self.ship.attributes[Attribute.maxTargets]
    except (AttributeError, KeyError):
      return None

  @property
  def scanStrength(self):
    """Returns the scan strength of the ship."""
    try:
      shipAttribs = self.ship.attributes
    except AttributeError:
      return None

    try:
      radar = shipAttribs[Attribute.scanRadarStrength]
      ladar = shipAttribs[Attribute.scanLadarStrength]
      magnetometric = shipAttribs[Attribute.scanMagnetometricStrength]
      gravimetric = shipAttribs[Attribute.scanGravimetricStrength]
    except KeyError:
      return None

    return radar or ladar or magnetometric or gravimetric

  @property
  def capacitor(self):
    """Returns details about the ship's capacitor.

    Returns:
      Dictionary in the form: {
        capacity: Capacitor capacity as a float.
        recharge: Capacitor recharge time as a float.
      }
    """
    try:
      shipAttribs = self.ship.attributes
    except AttributeError:
      return None

    try:
      capacity = shipAttribs[Attribute.capacitorCapacity]
      recharge = shipAttribs[Attribute.capacitorRecharge]
    except KeyError:
      return None

    recharge /= 1000 # milliseconds

    return {
        "capacity": capacity,
        "recharge": recharge,
    }

  @property
  def shield(self):
    """Returns details about the ship's shield.

    Returns:
      A dictionary containing:
        capacity: Shield capacity.
        recharge: Recharge time.
        resists: Dictionary in the form {
          em: EM resistance.
          explosive: Explosive resistance.
          kinetic: Kinetic resistance.
          thermal: Thermal resistance.
        }
    """
    try:
      shipAttribs = self.ship.attributes
    except AttributeError:
      return None

    try:
      capacity = shipAttribs[Attribute.shieldCapacity]
      recharge = shipAttribs[Attribute.shieldRecharge]
      em = shipAttribs[Attribute.shieldEM]
      explosive = shipAttribs[Attribute.shieldExplosive]
      kinetic = shipAttribs[Attribute.shieldKinetic]
      thermal = shipAttribs[Attribute.shieldThermal]
    except KeyError:
      return None

    recharge /= 1000 # milliseconds

    return {
        "capacity": capacity,
        "recharge": recharge,
        "resists": {
            "em": 1.0 - em,
            "explosive": 1.0 - explosive,
            "kinetic": 1.0 - kinetic,
            "thermal": 1.0 - thermal
        }
    }

  @property
  def armor(self):
    """Returns details about the ship's armor.

    Returns:
      A dictionary containing:
        capacity: Shield capacity.
        resists: Dictionary in the form {
          em: EM resistance.
          explosive: Explosive resistance.
          kinetic: Kinetic resistance.
          thermal: Thermal resistance.
        }
    """
    try:
      shipAttribs = self.ship.attributes
    except AttributeError:
      return None

    try:
      capacity = shipAttribs[Attribute.armorCapacity]
      em = shipAttribs[Attribute.armorEM]
      explosive = shipAttribs[Attribute.armorExplosive]
      kinetic = shipAttribs[Attribute.armorKinetic]
      thermal = shipAttribs[Attribute.armorThermal]
    except KeyError:
      return None

    return {
        "capacity": capacity,
        "resists": {
            "em": 1.0 - em,
            "explosive": 1.0 - explosive,
            "kinetic": 1.0 - kinetic,
            "thermal": 1.0 - thermal
        }
    }

  @property
  def hull(self):
    """Returns details about the ship's hull.

    Returns:
      A dictionary containing:
        capacity: Shield capacity.
        resists: Dictionary in the form {
          em: EM resistance.
          explosive: Explosive resistance.
          kinetic: Kinetic resistance.
          thermal: Thermal resistance.
        }
    """
    try:
      shipAttribs = self.ship.attributes
    except AttributeError:
      return None

    try:
      capacity = shipAttribs[Attribute.hullCapacity]
      em = shipAttribs[Attribute.hullEM]
      explosive = shipAttribs[Attribute.hullExplosive]
      kinetic = shipAttribs[Attribute.hullKinetic]
      thermal = shipAttribs[Attribute.hullThermal]
    except KeyError:
      return None

    return {
        "capacity": capacity,
        "resists": {
            "em": 1.0 - em,
            "explosive": 1.0 - explosive,
            "kinetic": 1.0 - kinetic,
            "thermal": 1.0 - thermal
        }
    }

  @property
  def alignTime(self):
    """Returns the time needed for the ship to enter warp.

    Returns:
      Floating point number representing align time in seconds.
    """
    try:
      shipAttribs = self.ship.attributes
    except AttributeError:
      return None

    try:
      agility = shipAttribs[Attribute.agility]
      mass = shipAttribs[Attribute.mass]
    except KeyError:
      return None

    alignTime = -math.log(0.25) * agility * mass / 1000000
    return alignTime

