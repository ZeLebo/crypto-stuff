import { makePublicKey, sharedSecret, randomSecret } from './crypto.js';
import { encryptMessage, decryptMessage } from './cipher.js';

export const runMitmScenario = (victimA, victimB, attacker, params, message) => {
  const attackerSecretA = attacker.secret;
  const attackerSecretB = randomSecret(params.P);
  const publicToA = attacker.publicKey;
  const publicToB = makePublicKey(params.G, attackerSecretB, params.P);

  const victimAPublic = victimA.publicKey;
  const victimBPublic = victimB.publicKey;

  const sharedVictimA = sharedSecret(publicToA, victimA.secret, params.P);
  const sharedVictimB = sharedSecret(publicToB, victimB.secret, params.P);

  const sharedWithA = sharedSecret(victimAPublic, attackerSecretA, params.P);
  const sharedWithB = sharedSecret(victimBPublic, attackerSecretB, params.P);

  const cipherFromA = encryptMessage(message, sharedVictimA);
  const attackerRead = decryptMessage(cipherFromA, sharedWithA);

  const forged = `${attacker.name}: ${attackerRead.replace(/[^\w\s:-]/g, '')} [изменено]`;
  const cipherToB = encryptMessage(forged, sharedWithB);
  const delivered = decryptMessage(cipherToB, sharedVictimB);

  return {
    publicParams: { P: params.P, G: params.G },
    parties: { victimA, victimB, attacker },
    attackerPublic: { toA: publicToA, toB: publicToB },
    secrets: {
      attackerA: attackerSecretA,
      attackerB: attackerSecretB,
      victimA: victimA.secret,
      victimB: victimB.secret
    },
    victimPublic: {
      a: victimAPublic,
      b: victimBPublic
    },
    wire: {
      fromVictim: cipherFromA,
      toVictim: cipherToB
    },
    shared: {
      victimA: sharedVictimA,
      victimB: sharedVictimB,
      attackerWithA: sharedWithA,
      attackerWithB: sharedWithB
    },
    plain: {
      sentByA: message,
      seenByAttacker: attackerRead,
      deliveredToB: delivered
    }
  };
};
