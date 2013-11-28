from .const import Attribute

import math


class Raven(object):
  """High level stats calculator for Eos fits."""

  def __init__(self, fit):
    self.fit = fit
    self._ship = fit.ship

    # Hardcode this here since it's not in any table.
    self.baseWarpSpeed = 3

  def _getAttribute(self, attrID, default = None):
    try:
      return self._ship.attributes[attrID]
    except (AttributeError, KeyError):
      return default or None

  @property
  def scanResolution(self):
    """Returns the scan resolution in mm of the ship."""
    return self._getAttribute(Attribute.scanResolution)

  @property
  def targetRange(self):
    """Returns the max target range in metres of the ship."""
    return self._getAttribute(Attribute.targetRange)

  @property
  def maxTargets(self):
    """Returns the max number of locked targets."""
    return self._getAttribute(Attribute.maxTargets)

  @property
  def sensorStrength(self):
    """Returns the sensor strength of the ship."""
    # TODO: also return type of sensor
    radar = self._getAttribute(Attribute.scanRadarStrength)
    ladar = self._getAttribute(Attribute.scanLadarStrength)
    magnetometric = self._getAttribute(Attribute.scanMagnetometricStrength)
    gravimetric = self._getAttribute(Attribute.scanGravimetricStrength)

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
    capacity = self._getAttribute(Attribute.capacitorCapacity)
    recharge = self._getAttribute(Attribute.capacitorRecharge)

    recharge /= 1000 # milliseconds

    return {
        "capacity": capacity,
        "recharge": recharge,
    }

  @property
  def shield(self):
    """Returns details about the ship's shield.

    Resists are integers from 0 to 100.

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
    capacity = self._getAttribute(Attribute.shieldCapacity)
    recharge = self._getAttribute(Attribute.shieldRecharge)
    em = self._getAttribute(Attribute.shieldEM)
    explosive = self._getAttribute(Attribute.shieldExplosive)
    kinetic = self._getAttribute(Attribute.shieldKinetic)
    thermal = self._getAttribute(Attribute.shieldThermal)

    recharge /= 1000 # milliseconds
    em = 1.0 - em
    explosive = 1.0 - explosive
    kinetic = 1.0 - kinetic
    thermal = 1.0 - thermal

    return {
        "capacity": capacity,
        "recharge": recharge,
        "resists": {
            "em": em,
            "explosive": explosive,
            "kinetic": kinetic,
            "thermal": thermal
        }
    }

  @property
  def armor(self):
    """Returns details about the ship's armor.

    Resists are integers from 0 to 100.

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
    capacity = self._getAttribute(Attribute.armorCapacity)
    em = self._getAttribute(Attribute.armorEM)
    explosive = self._getAttribute(Attribute.armorExplosive)
    kinetic = self._getAttribute(Attribute.armorKinetic)
    thermal = self._getAttribute(Attribute.armorThermal)

    em = 1.0 - em
    explosive = 1.0 - explosive
    kinetic = 1.0 - kinetic
    thermal = 1.0 - thermal

    return {
        "capacity": capacity,
        "resists": {
            "em": em,
            "explosive": explosive,
            "kinetic": kinetic,
            "thermal": thermal
        }
    }

  @property
  def hull(self):
    """Returns details about the ship's hull.

    Resists are integers from 0 to 100.

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
    capacity = self._getAttribute(Attribute.hullCapacity)
    em = self._getAttribute(Attribute.hullEM)
    explosive = self._getAttribute(Attribute.hullExplosive)
    kinetic = self._getAttribute(Attribute.hullKinetic)
    thermal = self._getAttribute(Attribute.hullThermal)

    em = 1.0 - em
    explosive = 1.0 - explosive
    kinetic = 1.0 - kinetic
    thermal = 1.0 - thermal

    return {
        "capacity": capacity,
        "resists": {
            "em": em,
            "explosive": explosive,
            "kinetic": kinetic,
            "thermal": thermal
        }
    }

  @property
  def mass(self):
    """Returns the mass of the ship in kg."""
    return self._getAttribute(Attribute.mass)

  @property
  def agility(self):
    """Returns the agility of the ship."""
    return self._getAttribute(Attribute.agility)

  @property
  def speed(self):
    """Returns the max speed of the ship in m/s."""
    return self._getAttribute(Attribute.maxVelocity)

  @property
  def signatureRadius(self):
    """Returns the signature radius of the ship."""
    return self._getAttribute(Attribute.signatureRadius)

  @property
  def warpSpeed(self):
    """Returns the warp speed of the ship in AU/s."""
    multiplier = self._getAttribute(Attribute.warpSpeedMultiplier)

    return multiplier * self.baseWarpSpeed

  @property
  def alignTime(self):
    """Returns the time needed for the ship to enter warp.

    Returns:
      Floating point number representing align time in seconds.
    """
    agility = self.agility
    mass = self.mass

    alignTime = -math.log(0.25) * agility * mass / 1000000
    return alignTime

  @property
  def slots(self):
    """Get the number of slots for a given ship.

    Returns:
      A dictionary.
    """
    highSlots = self._getAttribute(Attribute.highSlots)
    medSlots = self._getAttribute(Attribute.medSlots)
    lowSlots = self._getAttribute(Attribute.lowSlots)

    if None in [highSlots, medSlots, lowSlots]:
      # This is a T3 ship.
      highSlots = medSlots = lowSlots = 0

    # Get rigs and subs.
    rigSlots = self._getAttribute(Attribute.rigSlots, 0)
    subSlots = self._getAttribute(Attribute.subSlots, 0)

    # Get missile and turret slots.
    missileSlots = self._getAttribute(Attribute.missileSlots, 0)
    turretSlots = self._getAttribute(Attribute.turretSlots, 0)

    return {
        "highSlots": int(highSlots),
        "medSlots": int(medSlots),
        "lowSlots": int(lowSlots),
        "rigSlots": int(rigSlots),
        "subSlots": int(subSlots),
        "turretSlots": int(turretSlots),
        "missileSlots": int(missileSlots)
    }

  def _ehp(self, layer, multipliers):
    em = layer["capacity"] / (1 - layer["resists"]["em"])
    explosive = layer["capacity"] / (1 - layer["resists"]["explosive"])
    kinetic = layer["capacity"] / (1 - layer["resists"]["kinetic"])
    thermal = layer["capacity"] / (1 - layer["resists"]["thermal"])

    raw = [em, explosive, kinetic, thermal]
    total = 0
    for k, v in enumerate(raw):
      total += v * multipliers[k]

    return total

  def get_ehp(self, damageProfile = None):
    """Get effective hitpoints of ship based on given damage profile.

    Args:
      damageProfile: Incoming damage distribution in the form
      [em, explosive, kinetic, thermal]

    Returns:
      A dictionary containing the effective hitpoints for shield, armor and
      hull.
    """
    if damageProfile is None:
      damageProfile = [1, 1, 1, 1]

    totalDamage = sum(damageProfile)
    emMultiplier = damageProfile[0] / totalDamage
    explosiveMultiplier = damageProfile[1] / totalDamage
    kineticMultiplier = damageProfile[2] / totalDamage
    thermalMultiplier = 1.0 - emMultiplier - explosiveMultiplier - kineticMultiplier

    multipliers = [emMultiplier, explosiveMultiplier, kineticMultiplier, thermalMultiplier]

    effectiveShield = self._ehp(self.shield, multipliers)
    effectiveArmor = self._ehp(self.armor, multipliers)
    effectiveHull = self._ehp(self.hull, multipliers)

    return {
        "shield": effectiveShield,
        "armor": effectiveArmor,
        "hull": effectiveHull
    }

